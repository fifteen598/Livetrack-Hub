// LocationTracker.swift
import CoreLocation
import SwiftUI

// Location Sharing Service
class LocationSharingService {
    private let serverURL = "https://fifteen598.pythonanywhere.com/update_location"
    
    func shareLocation(_ location: CLLocation, userName: String, isDemoMode: Bool) {
        if isDemoMode {
            print("DEMO MODE: Location would be sent for \(userName): \(location.coordinate.latitude), \(location.coordinate.longitude)")
            return
        }
        
        let locationData = [
            "name": userName,
            "latitude": location.coordinate.latitude,
            "longitude": location.coordinate.longitude
        ] as [String : Any]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: locationData) else {
            print("Error: Cannot create JSON from location data")
            return
        }
        
        guard let url = URL(string: serverURL) else {
            print("Error: Invalid server URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending location: \(error)")
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Server response: \(httpResponse.statusCode)")
            }
        }.resume()
    }
}

// Location Tracker
class LocationTracker: NSObject, ObservableObject {
    @Published var locations: [CLLocation] = []
    @Published var lastLocation: CLLocation?
    @Published var isTracking = false
    @Published var isDemoMode = false
    @Published var userName: String = UserDefaults.standard.string(forKey: "userName") ?? "USER"
    
    private let locationManager = CLLocationManager()
    private let sharingService = LocationSharingService()
    
    override init() {
        super.init()
        setupLocationManager()
    }
    
    private func setupLocationManager() {
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.pausesLocationUpdatesAutomatically = false
        locationManager.distanceFilter = 10 // Update every 10 meters
        locationManager.activityType = .fitness
    }
    
    func startTracking() {
        isTracking = true
        
        // Clear locations when starting new tracking session
        locations.removeAll()
        
        let authStatus = locationManager.authorizationStatus
        if authStatus == .notDetermined {
            locationManager.requestAlwaysAuthorization()
        } else if authStatus == .authorizedWhenInUse || authStatus == .authorizedAlways {
            locationManager.startUpdatingLocation()
        } else {
            // Show alert or handle denied/restricted permissions
            print("Location permission denied or restricted")
        }
    }
    
    func stopTracking() {
        locationManager.stopUpdatingLocation()
        isTracking = false
    }
    
    func clearLocationHistory() {
        locations.removeAll()
    }
    
    // Function to generate a simulated location for demo mode
    func simulateLocationUpdate() {
        guard isTracking && isDemoMode else { return }
        
        // Create a random location near Wichita State University
        let baseLatitude = 37.7178
        let baseLongitude = -97.2921
        
        let randomLatOffset = Double.random(in: -0.005...0.005)
        let randomLongOffset = Double.random(in: -0.005...0.005)
        
        let simulatedLocation = CLLocation(
            coordinate: CLLocationCoordinate2D(
                latitude: baseLatitude + randomLatOffset,
                longitude: baseLongitude + randomLongOffset
            ),
            altitude: Double.random(in: 400...450),
            horizontalAccuracy: 10,
            verticalAccuracy: 10,
            timestamp: Date()
        )
        
        // Process the simulated location
        self.lastLocation = simulatedLocation
        self.locations.append(simulatedLocation)
        
        // Share the simulated location
        sharingService.shareLocation(simulatedLocation, userName: userName, isDemoMode: isDemoMode)
    }
}

extension LocationTracker: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard !isDemoMode, let location = locations.last else { return }
        
        self.lastLocation = location
        self.locations.append(location)
        
        // Send location to server
        sharingService.shareLocation(location, userName: userName, isDemoMode: isDemoMode)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Location error: \(error.localizedDescription)")
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .authorizedAlways, .authorizedWhenInUse:
            if isTracking {
                locationManager.startUpdatingLocation()
            }
        case .notDetermined:
            locationManager.requestAlwaysAuthorization()
        case .restricted, .denied:
            print("Location access restricted or denied")
        @unknown default:
            break
        }
    }
}
