// LiveTrackApp.swift
import SwiftUI
import CoreLocation

@main
struct LiveTrackApp: App {
    // Init life cycle delegate to handle app state changes
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// App Delegate to handle background tasks
class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        // Request notification permissions if needed for location updates
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if granted {
                print("Notification permission granted")
            } else if let error = error {
                print("Notification error: \(error)")
            }
        }
        return true
    }
    
    // Handle when app enters background
    func applicationDidEnterBackground(_ application: UIApplication) {
        print("App entered background")
    }
    
    // Handle when app becomes active
    func applicationDidBecomeActive(_ application: UIApplication) {
        print("App became active")
    }
}
