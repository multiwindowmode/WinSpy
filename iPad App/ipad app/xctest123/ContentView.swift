import SwiftUI

struct ContentView: View {

    var viewModel: ThreadManager
    @State private var currentIndex = 0
    
    let urls = [
        "https://m.baidu.com",
        "https://m.sina.com.cn",
        "https://m.taobao.com",
        "https://m.weibo.com",
        "https://m.zhihu.com",
        "https://www.douyin.com",
        "https://m.jd.com"
    ]
    
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
            Button(action: {
                self.currentIndex = (self.currentIndex + 1) % self.urls.count
                if let url = URL(string: self.urls[self.currentIndex]) {
                    if UIApplication.shared.canOpenURL(url) {
                        UIApplication.shared.open(url, options: [:], completionHandler: nil)
                    }
                }
                }) {
                    Text("Open Browser")
                        .font(.title2)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
        }
        .padding()
    }
}
