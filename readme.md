**WinSpy** is a cross-window side-channel attack approach that targets Android's multi-window mode. It exploits the resource competition between apps running concurrently to perform various attacks without violating Android's permission frameworks.

### Key Points About WinSpy:

1. **Cross-window Side-channel Attacks**:
    - **Resource Competition**: WinSpy leverages the competition for resources like CPU, memory, and disk usage among apps in multi-window mode. By monitoring these resources, it can infer sensitive information.
    - **Shared Sensor Readings**: WinSpy uses shared sensor readings (e.g., accelerometer, gyroscope) to gather data that can be used to deduce user interactions and actions in other apps.

2. **Types of Attacks**:
    - **App Launch Fingerprinting**: Identifies the start of an app based on the resource usage patterns during its launch.
    - **Website Launch Fingerprinting**: Recognizes the website being browsed by monitoring resource allocation when a web page is loaded.
    - **In-app Activities Fingerprinting**: Detects specific user activities within an app, such as typing or interacting with certain features, by analyzing resource competition.
    - **IMU-based Tap Location Inference**: Infers the tap positions on the screen based on the motion sensor data, potentially revealing user inputs.
    - **IMU-based Sound Recovery**: Recovers audio played by the victim app using the motion sensor data to reconstruct the sound vibrations.

### Directory Structure

```plaintext
WinSpy
├── ADB control
│   ├── inner_app_chat
│   ├── inner_app_pay
│   ├── open_app
│   ├── open_app_background
│   └── open_website
├── Collected Data
│   ├── App Lanuch
│   ├── In-app Operations
│   │   ├── inner_app_Alipay
│   │   └── inner_app_WhatsApp
│   ├── Sound Recovery
│   ├── Tap Inference
│   └── Website Lanuch
├── Resouce Competition Apps
│   ├── profiler2cmd5
│   └── Profiler2Cpu5
├── Sound Recovery Android Apps
│   ├── Pair1_ImuRecorder
│   ├── Pair2_Speaker
│   └── Pair3_both
├── Tap Inference Android Apps
│  ├── TappingImu
│  ├── TappingImu10
│  ├── TappingImu10_phone
│  └── Tapping_ImuRecorder_Attacker
└── video recording of an experimental process.mkv
```

- **ADB control** directory contains our experimental control scripts. For example, `inner_app_chat` simulates human interactions with the phone screen by controlling clicks and swipes, allowing for repeated operations to collect data.
- **Collected Data** directory has five folders corresponding to the five types of experiments described in the paper. Unfortunately, due to the high frequency of CPU or IMU data collection, each single experiment record exceeds 100MB, which surpasses GitHub's limit. This part of the data will be made available through external links or by providing our contact information later.
- **Resource Competition Apps** directory contains two folders for the two types of apps used in the Resource Competition experiment. `profiler2cmd5` refers to apps that compete for three types of threads simultaneously, while `Profiler2Cpu5` only competes for CPU threads.
- **Sound Recovery Android Apps** directory contains three folders: an accelerometer data collection app, a voice playback app, and an app that combines both functions.
- **Tap Inference Android Apps** directory contains four folders. Three of them are tap inference input apps with different layouts. The `Tapping_ImuRecorder_Attacker` app runs in the window as an attacking app.

- **video recording** This is a video recording of an experimental process, documenting the proceedings of our 21 App launch experiments. Due to the need for privacy protection during the review phase, the video has been blurred and overexposed. We will replace it with a high-definition version once the paper is accepted.