//
//  xctest123UITests.swift
//  xctest123UITests
//
//  Created by 李增 on 2024-08-27.
//

import XCTest

final class xctest123UITests: XCTestCase {

    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.

        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false

        // In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    let app = XCUIApplication()
    
    func testExample() throws {
        // UI tests must launch the application that they test.
//        app.launch()

        // Use XCTAssert and related functions to verify your tests produce the correct results.
    }
    func testTapAtCoordinate() {
        let x = 1000
        let y = 1000
        let coordinate = app.coordinate(withNormalizedOffset: CGVector(dx: 0, dy: 0))
        let adjustedCoordinate = coordinate.withOffset(CGVector(dx: x, dy: y))
        adjustedCoordinate.tap()
    }
    
    func testLaunchPerformance() throws {
        if #available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 7.0, *) {
            // This measures how long it takes to launch your application.
            measure(metrics: [XCTApplicationLaunchMetric()]) {
                XCUIApplication().launch()
            }
        }
    }
}
