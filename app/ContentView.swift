// ContentView.swift
import SwiftUI
import CoreLocation

struct ContentView: View {
    @StateObject private var locationTracker = LocationTracker()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Status Card
                VStack(spacing: 16) {
                    HStack {
                        Image(systemName: locationTracker.isTracking ? "location.fill" : "location.slash.fill")
                            .foregroundColor(locationTracker.isTracking ? .green : .red)
                        Text(locationTracker.isTracking ? "Tracking Active" : "Tracking Inactive")
                            .font(.headline)
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.gray.opacity(0.1))
                    .cornerRadius(10)
                    
                    // Current Location Display
                    if let location = locationTracker.lastLocation {
                        VStack(alignment: .leading, spacing: 8) {
                            Label("Current Location", systemImage: "paperplane")
                                .font(.headline)
                            
                            LocationDataRow(title: "Latitude", value: location.coordinate.latitude)
                            LocationDataRow(title: "Longitude", value: location.coordinate.longitude)
                            LocationDataRow(title: "Altitude", value: location.altitude, unit: "m")
                            if location.speed >= 0 {
                                LocationDataRow(title: "Speed", value: location.speed, unit: "m/s")
                            }
                        }
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(10)
                    } else {
                        Text("Waiting for location...")
                            .foregroundColor(.gray)
                    }
                    
                    // Control Button
                    Button(action: {
                        if locationTracker.isTracking {
                            locationTracker.stopTracking()
                        } else {
                            locationTracker.startTracking()
                        }
                    }) {
                        HStack {
                            Image(systemName: locationTracker.isTracking ? "stop.fill" : "play.fill")
                            Text(locationTracker.isTracking ? "Stop Tracking" : "Start Tracking")
                        }
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(locationTracker.isTracking ? Color.red : Color.green)
                        .cornerRadius(10)
                    }
                }
                .padding()
                
                // Location History
                if !locationTracker.locations.isEmpty {
                    List {
                        ForEach(locationTracker.locations.indices, id: \.self) { index in
                            LocationHistoryRow(location: locationTracker.locations[index], index: index)
                        }
                    }
                } else {
                    ContentUnavailableView("No Location History",
                        systemImage: "location.slash",
                        description: Text("Start tracking to begin recording locations")
                    )
                }
            }
            .navigationTitle("LiveTrack")
        }
    }
}

struct LocationDataRow: View {
    let title: String
    let value: Double
    var unit: String = ""
    
    var body: some View {
        HStack {
            Text(title)
                .foregroundColor(.gray)
            Spacer()
            Text(String(format: "%.6f", value) + (unit.isEmpty ? "" : " \(unit)"))
                .fontWeight(.medium)
        }
    }
}

struct LocationHistoryRow: View {
    let location: CLLocation
    let index: Int
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Location \(index + 1)")
                .font(.headline)
            Text("Lat: \(location.coordinate.latitude, specifier: "%.6f")")
                .foregroundColor(.gray)
            Text("Long: \(location.coordinate.longitude, specifier: "%.6f")")
                .foregroundColor(.gray)
            Text(formatDate(location.timestamp))
                .font(.caption)
                .foregroundColor(.blue)
        }
        .padding(.vertical, 4)
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .medium
        return formatter.string(from: date)
    }
}
