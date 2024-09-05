import Foundation
import SwiftUI


class Timer1 {
    static let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSS"  // 包括到毫秒
        return formatter
    }()
    
    static let dateFormatter2: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSSSSS"
        return formatter
    }()

    static func getCurrentTime() -> String {
        let now = Date()
        return Timer1.dateFormatter.string(from: now)
    }
    
    static func getCurrentTime2() -> String {
        let now = Date()
        return Timer1.dateFormatter2.string(from: now) + "+08:00"
    }
}


class FileWriterAndr {
    private let fileURL: URL
    private var fileHandle: FileHandle?

    init() {
        let fileManager = FileManager.default
        let urls = fileManager.urls(for: .documentDirectory, in: .userDomainMask)
        let documentDirectory = urls[0]
        self.fileURL = documentDirectory.appendingPathComponent("andr.txt")

        if !fileManager.fileExists(atPath: fileURL.path) {
            fileManager.createFile(atPath: fileURL.path, contents: nil, attributes: nil)
        }
        
        do {
            fileHandle = try FileHandle(forWritingTo: fileURL)
            fileHandle?.seekToEndOfFile()
        } catch {
            print("Unable to open file: \(error)")
        }
    }
    
    deinit {
        fileHandle?.closeFile()
    }

    func appendToFile(_ data: String) {
        guard let fileHandle = fileHandle, let data = (data + "\n").data(using: .utf8) else {
            print("Error: Unable to write to file.")
            return
        }
        fileHandle.write(data)
    }
}

class FileWriterLog {
    private let fileURL: URL
    private var fileHandle: FileHandle?

    init() {
        let fileManager = FileManager.default
        let urls = fileManager.urls(for: .documentDirectory, in: .userDomainMask)
        let documentDirectory = urls[0]
        self.fileURL = documentDirectory.appendingPathComponent("log.txt")

        if !fileManager.fileExists(atPath: fileURL.path) {
            fileManager.createFile(atPath: fileURL.path, contents: nil, attributes: nil)
        }
        
        do {
            fileHandle = try FileHandle(forWritingTo: fileURL)
            fileHandle?.seekToEndOfFile()
        } catch {
            print("Unable to open file: \(error)")
        }
    }
    
    deinit {
        fileHandle?.closeFile()
    }

    func appendToFile(_ data: String) {
        guard let fileHandle = fileHandle, let data = (data + "\n").data(using: .utf8) else {
            print("Error: Unable to write to file.")
            return
        }
        fileHandle.write(data)
    }
}


class TaskWorker {
    private var count = Int64(0)
    private var u = Double(1.0)
    
    func startTask() {
        DispatchQueue.global().async {
            while true {
                self.u = exp(self.u + 1.0)
                self.u = log(self.u + abs(sin(self.u)))
                self.u = sin(self.u)
                self.u = pow(self.u, 2.0)
                self.u = sqrt(abs(self.u))
                self.u = atan(self.u)
                self.u = abs(self.u) / (abs(self.u) + 1) + 1
                self.count += 1
            }
        }
    }
    
    func getResult() -> (count: Int64, u: Double) {
        return (count, u)
    }
}

class ThreadManager{
    
    var totalCnt: Int64 = 0
    var totalU: Double = 0
    private let andrWriter = FileWriterAndr()
    private let logWriter = FileWriterLog()

    private var workers: [TaskWorker]
    private let numberOfThreads: Int
    
    init(numberOfThreads: Int) {
        self.numberOfThreads = numberOfThreads
        self.workers = (0..<numberOfThreads).map { _ in TaskWorker() }
    }
    
    let urls = [
        "https://youku.com",
        "https://m.sina.com.cn",
        "https://m.taobao.com",
        "https://m.weibo.com",
        "https://m.zhihu.com",
        "https://www.douyin.com",
        "https://m.jd.com"
    ]
    private var currentIndex = 0
    
    func start() {
        for worker in workers {
            worker.startTask()
        }
        
        let monitoringThread = Thread {
            var ji = 0
            while true {
                usleep(10000) // 10 ms
                var tempTotalCnt = Int64(0)
                var tempTotalU = Double(0.0)
                for worker in self.workers {
                    let res = worker.getResult()
                    tempTotalCnt += res.count
                    tempTotalU += res.u
                }
                self.andrWriter.appendToFile("\(Timer1.getCurrentTime()) \(tempTotalCnt - self.totalCnt) 0 0")
                ji += 1
                if ji % 100 == 0 {
                    print("Total loop counts: \(Timer1.getCurrentTime()) \(tempTotalCnt - self.totalCnt) \(self.totalU)")
                }
                self.totalCnt = tempTotalCnt
                self.totalU = tempTotalU
            }
        }
        monitoringThread.qualityOfService = .userInteractive
        monitoringThread.start()
        
        DispatchQueue.global(qos: .userInteractive).async {
            while true {
                usleep(10_000_000)

                DispatchQueue.main.async {
                    self.currentIndex = (self.currentIndex + 1) % self.urls.count
                    if let url = URL(string: self.urls[self.currentIndex]) {
                        self.logWriter.appendToFile("\(url) \(Timer1.getCurrentTime2())")
                        if UIApplication.shared.canOpenURL(url) {
                            UIApplication.shared.open(url, options: [:], completionHandler: nil)
                        }
                    }
                }
            }
        }
    }
}
