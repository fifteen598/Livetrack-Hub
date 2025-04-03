// ContentView.swift
import SwiftUI
import CoreLocation

struct ContentView: View {
    @StateObject private var locationTracker = LocationTracker()
    @State private var showingNamePrompt = false
    @State private var lastUpdateTime: Date?
    @State private var demoTimer: Timer?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 16) {
                // Status Card
                VStack(spacing: 16) {
                    // Tracking Status
                    HStack {
                        Image(systemName: locationTracker.isTracking ? "location.fill" : "location.slash.fill")
                            .foregroundColor(locationTracker.isTracking ? .green : .red)
                        Text(locationTracker.isTracking ? "Tracking Active" : "Tracking Inactive")
                            .font(.headline)
                        
                        if locationTracker.isDemoMode {
                            Text("(Demo)")
                                .font(.caption)
                                .foregroundColor(.orange)
                                .padding(.leading, 4)
                        }
                        
                        Spacer()
                        
                        // Demo mode toggle
                        Toggle("", isOn: $locationTracker.isDemoMode)
                            .labelsHidden()
                            .onChange(of: locationTracker.isDemoMode) { oldValue, newValue in
                                if locationTracker.isTracking {
                                    stopTracking()
                                    startTracking()
                                }
                            }
                    }
                    .padding()
                    .background(Color.gray.opacity(0.1))
                    .cornerRadius(10)
                    
                    // Current Location Display
                    if let location = locationTracker.lastLocation {
                        VStack(alignment: .leading, spacing: 8) {
                            Label("Current Location", systemImage: "paperplane")
                                .font(.headline)
                            
                            LocationDataRow(title: "Latitude", value: location.coordinate.latitude)
                            LocationDataRow(title: "Longitude", value: location.coordinate.longitude)
                        }
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(10)
                    } else {
                        Text("Waiting for location...")
                            .foregroundColor(.gray)
                            .frame(height: 100)
                            .frame(maxWidth: .infinity)
                            .background(Color.gray.opacity(0.1))
                            .cornerRadius(10)
                    }
                    
                    // Control Buttons
                    HStack(spacing: 16) {
                        // Start/Stop Button
                        Button(action: {
                            if locationTracker.isTracking {
                                stopTracking()
                            } else {
                                startTracking()
                            }
                        }) {
                            HStack {
                                Image(systemName: locationTracker.isTracking ? "stop.fill" : "play.fill")
                                Text(locationTracker.isTracking ? "Stop" : "Start")
                            }
                            .foregroundColor(.white)
                            .padding()
                            .frame(maxWidth: .infinity)
                            .background(locationTracker.isTracking ? Color.red : Color.green)
                            .cornerRadius(10)
                        }
                        
                        // Reset Button
                        Button(action: {
                            locationTracker.clearLocationHistory()
                        }) {
                            HStack {
                                Image(systemName: "arrow.counterclockwise")
                                Text("Reset")
                            }
                            .foregroundColor(.white)
                            .padding()
                            .frame(maxWidth: .infinity)
                            .background(Color.gray)
                            .cornerRadius(10)
                        }
                    }
                }
                .padding(.horizontal)
                
                // Location History - Apple Stopwatch Style
                VStack(alignment: .leading, spacing: 8) {
                    Text("Location History")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    if locationTracker.locations.isEmpty {
                        Text("No locations recorded")
                            .foregroundColor(.gray)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 40)
                    } else {
                        ScrollView {
                            VStack(spacing: 0) {
                                ForEach(locationTracker.locations.indices.reversed(), id: \.self) { index in
                                    LocationLogRow(
                                        location: locationTracker.locations[index],
                                        count: locationTracker.locations.count - index
                                    )
                                    
                                    if index > 0 {
                                        Divider()
                                            .padding(.leading, 60)
                                    }
                                }
                            }
                            .padding(.horizontal)
                        }
                    }
                }
                .frame(maxHeight: .infinity)
                .background(Color(.systemBackground))
            }
            .navigationTitle("LiveTrack")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingNamePrompt = true }) {
                        HStack {
                            Text(locationTracker.userName)
                                .font(.subheadline)
                            Image(systemName: "person.circle")
                        }
                    }
                }
            }
            .alert("Enter Your Name", isPresented: $showingNamePrompt) {
                TextField("Name", text: $locationTracker.userName)
                Button("Save") {
                    UserDefaults.standard.set(locationTracker.userName, forKey: "userName")
                }
            } message: {
                Text("This will be sent with your location data")
            }
            .onChange(of: locationTracker.lastLocation) { oldValue, newValue in
                lastUpdateTime = Date()
            }
        }
    }
    
    private func startTracking() {
        locationTracker.startTracking()
        
        if locationTracker.isDemoMode {
            demoTimer?.invalidate()
            demoTimer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { _ in
                locationTracker.simulateLocationUpdate()
            }
            locationTracker.simulateLocationUpdate()
        }
    }
    
    private func stopTracking() {
        locationTracker.stopTracking()
        demoTimer?.invalidate()
        demoTimer = nil
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
                .monospaced()
        }
    }
}

struct LocationLogRow: View {
    let location: CLLocation
    let count: Int
    
    var body: some View {
        HStack(spacing: 16) {
            // Lap number/count
            Text("\(count)")
                .font(.system(size: 18, weight: .semibold, design: .rounded))
                .frame(width: 40, alignment: .center)
            
            // Location details
            VStack(alignment: .leading, spacing: 2) {
                Text(formatTime(location.timestamp))
                    .font(.system(size: 17, weight: .medium))
                
                Text("\(location.coordinate.latitude, specifier: "%.5f"), \(location.coordinate.longitude, specifier: "%.5f")")
                    .font(.system(size: 14, design: .monospaced))
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            // Distance if available
            if count > 1 {
                Text(formatDistanceFromPrevious(location, count: count))
                    .font(.system(size: 15))
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 10)
    }
    
    private func formatTime(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "h:mm:ss a"
        return formatter.string(from: date)
    }
    
    private func formatDistanceFromPrevious(_ location: CLLocation, count: Int) -> String {
        // This would ideally calculate distance from previous point
        // For now, just return a placeholder
        return ""
    }
}
