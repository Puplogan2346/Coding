import SwiftUI
import WebKit

struct TutorWebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true
        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.allowsBackForwardNavigationGestures = true
        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        if webView.url != url {
            webView.load(URLRequest(url: url))
        }
    }
}

struct ContentView: View {
    // Use localhost in the iOS Simulator when the Streamlit app is running on your Mac.
    // If it does not load, replace this with your Mac's local IP address, for example:
    // URL(string: "http://192.168.1.25:8501")!
    private let appURL = URL(string: "http://localhost:8501")!

    var body: some View {
        TutorWebView(url: appURL)
            .ignoresSafeArea()
    }
}

#Preview {
    ContentView()
}
