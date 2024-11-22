// LocationTracker.swift
import CoreLocation
import SwiftUI

// Location Sharing Service
class LocationSharingService {
    private let serverURL = "http://SERVER_IP:5000/update_location"
    private let userName = "NAME" // Replace with your name
    
    func shareLocation(_ location: CLLocation) {
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
                print("Flask server response: \(httpResponse.statusCode)")
            }
        }.resume()
    }
}

// Location Tracker
class LocationTracker: NSObject, ObservableObject {
    @Published var locations: [CLLocation] = []
    @Published var lastLocation: CLLocation?
    @Published var isTracking = false
    
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
        locationManager.requestAlwaysAuthorization()
        isTracking = true
    }
    
    func stopTracking() {
        locationManager.stopUpdatingLocation()
        isTracking = false
    }
}

extension LocationTracker: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        self.lastLocation = location
        self.locations.append(location)
        
        // Send location to Flask server
        sharingService.shareLocation(location)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Location error: \(error)")
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .authorizedAlways:
            locationManager.startUpdatingLocation()
        case .authorizedWhenInUse:
            locationManager.requestAlwaysAuthorization()
        case .notDetermined, .restricted, .denied:
            print("Location access not granted")
        @unknown default:
            break
        }
    }
}
