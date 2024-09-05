import SwiftUI

@main
struct xctest123App: App {
    
    private var viewModel = ThreadManager(numberOfThreads: 8)
    
    var body: some Scene {
        WindowGroup {
            ContentView(viewModel: viewModel).onAppear {
                viewModel.start()
            }
        }
    }
    
}
