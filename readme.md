**WinSpy** is a cross-window side-channel attack approach that targets Android's multi-window mode. It exploits the resource contention between apps running concurrently to perform various attacks without violating Android's permission frameworks.

### Key Points About WinSpy:

1. **Cross-window Side-channel Attacks**:
    - **Resource Contention**: WinSpy leverages the contention for resources like CPU, memory, and disk usage among apps in multi-window mode. By monitoring these resources, it can infer sensitive information.
    - **Shared Sensor Readings**: WinSpy uses shared sensor readings (e.g., accelerometer, gyroscope) to gather data that can be used to deduce user interactions and actions in other apps.

2. **Types of Attacks**:
    - **App Launch Fingerprinting**: Identifies the start of an app based on the resource contention patterns during its launch.
    - **Website Launch Fingerprinting**: Recognizes the website being browsed by monitoring resource contention when a web page is loaded.
    - **In-app Activities Fingerprinting**: Detects specific user activities within an app, such as typing or interacting with certain features, by analyzing resource contention.
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
│   ├── App Launch
│   ├── In-app Operations
│   │   ├── inner_app_Alipay
│   │   └── inner_app_WhatsApp
│   ├── Sound Recovery
│   ├── Tap Inference
│   └── Website Launch
├── iPad App
├── Resouce Contention Apps
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
- **Resource Contention Apps** directory contains two folders for the two types of apps used in the Resource Contention experiment. `profiler2cmd5` refers to apps that contend for three types of threads simultaneously, while `Profiler2Cpu5` only contends for CPU threads.
- **Sound Recovery Android Apps** directory contains three folders: an accelerometer data collection app, a voice playback app, and an app that combines both functions.
- **Tap Inference Android Apps** directory contains four folders. Three of them are tap inference input apps with different layouts. The `Tapping_ImuRecorder_Attacker` app runs in the window as an attacking app.

- **video recording** This is a video recording of an experimental process, documenting the proceedings of our 21 App launch experiments. Due to the need for privacy protection during the review phase, the video has been blurred and overexposed. We will replace it with a high-definition version once the paper is accepted.

### Supplemental Material of the paper
1. **How We Use ADB Commands to Automate Experiments**

Android Debug Bridge (ADB) is a versatile command-line tool that allows users to communicate with a connected Android device. ADB commands can perform a range of actions from basic device interactions to more complex tasks. Below is a table highlighting part of the key functionalities we used:

| Command | Description |
|---------|-------------|
| `adb shell input tap x y` | Simulates a tap on the screen at coordinates (x, y). |
| `adb shell input swipe x1 y1 x2 y2` | Simulates a swipe from coordinates (x1, y1) to (x2, y2). |
| `adb shell input text 'abcd'` | Inputs the specified text into the current focus area. |
| `adb shell dumpsys battery` | Retrieves the battery state of the device. |
| `adb shell input keyevent KEYCODE_POWER` | Simulates pressing the power button (can toggle screen on/off). |
| `adb shell date` | Returns the current system date and time. |

2. **List of the 21 attacked apps (in App Launch Fingerprinting)**:

| Category         | App(s)                                     |
|----------------------|------------------------------------------------|
| **Social Networks**  | Instagram, Facebook, TikTok, WeChat, LINE      |
| **Messaging**        | WhatsApp, Telegram, Messenger                  |
| **Content Streaming**| YouTube, Netflix, Spotify, Bilibili            |
| **Web Browsing**     | Google Chrome, Microsoft Edge, Mozilla Firefox |
| **Utilities**        | Google Maps, Google Translator, Gmail          |
| **Creative Platform**| Pixiv                                          |
| **Social Discovery** | Tinder                                         |
| **Gaming Platform**  | Steam                                          |

3. **Details of the 21 attacked websites  (in Website Launch Fingerprinting)**:

| Category                | Websites                                                       |
|-----------------------------|-----------------------------------------------------------------------------|
| **Tech & Media**            | google.com, facebook.com, instagram.com, twitter.com, baidu.com, yahoo.com  |
| **Entertainment**           | youtube.com, netflix.com, bilibili.com, twitch.tv                           |
| **eCommerce**               | amazon.com, ebay.com, paypal.com                                            |
| **Information & Reference** | wikipedia.org, quora.com, maps.google.com, deepl.com, indeed.com            |
| **Lifestyle**               | booking.com, weather.com, espn.com                                          |

4. **Test results for different types of threads and various quantities in adversary app**:

In our paper, we have already demonstrated our adversary app, which includes CPU threads and statistical threads. However, in our initial design, there were also two other types of resource contention threads: memory threads and disk threads. The detailed designs of these two types of threads are as follows:

- **Memory Thread:** The memory threads are designed to saturate memory bandwidth by continuously creating and destroying containers of specified sizes, as well as randomly altering their contents.

- **Disk Thread:** To maximize the usage of disk bandwidth, the disk threads continuously perform random read and write operations on files. The file size is 4KB, a commonly adopted standard in hard drive testing reports, as it effectively reflects the drive's speed with non-sequential storage locations and rapidly occupies the available bandwidth.


| Threads Allocation  | 3:1:1 | 6:2:2 | 9:3:3 | 5:0:0 | 10:0:0 | 15:0:0 |
|---------------------|-------|-------|-------|-------|--------|--------|
| **Accuracy**        | 73.4% | 72.2% | 41.8% | 81.5% | 90.7%  | 70.9%  |


The above table presents the accuracy of app launch fingerprinting attacks in identifying the launch of the seven different victim apps with varying numbers of resource-consuming threads. From left to right, until the third column, the number of threads for all three resources increases proportionally, leading to more intense competition. However, as mentioned earlier, a large number of threads can pose challenges for thread scheduling, causing instability in the adversary app. The accuracy of the attacks drops significantly to only 41.8\% when utilizing 9 CPU threads, 3 memory threads, and 3 disk threads, whereas a lightweight or medium thread setup maintains the accuracy above 72\%. We also evaluate thread allocations in which only CPU competition is introduced, as shown in columns 4-6 in Table. From the results, we can observe that CPU-only competition with a medium thread setup, i.e., 10 CPU threads in the adversary app, achieves the best attack accuracy of 90.7\% compared to other settings. The CPU-only thread settings achieve higher accuracy than the mixed thread settings because the tasks of CPU threads are basic computations, which are more lightweight than the tasks of memory and disk threads. Consequently, significantly more CPU tasks can be completed, providing a larger value range than its counterparts. This increased task completion potential allows for the observation of fine-grained characteristics during competition. In the following further evaluations on app launch fingerprinting, the CPU-only setting with 10 threads is chosen due to its superior performance in achieving higher attack accuracy. This setup ensures that the adversary app can effectively monitor and analyze resource consumption to identify different victim apps and their activities.  



4. **Generalization ability of Winspy on iOS**:

In our experiment on iOS, we used the 2021 iPad Pro (iOS 17.6.1) as the test device to assess the classification accuracy of seven websites in split-screen mode (Microsoft Edge + adversary app). However, due to the absence of convenient automation tools like the adb command, we directly allowed the adversary app to send URL open requests. Upon receiving the request, the system would automatically forward them to the default browser. Therefore, our adversary app includes two types of threads (CPU threads and statistics thread) and a URL sending thread, which randomly selects one of the seven URLs to send to the system every 10 seconds.

5. **IMU-based sound recovery of Winspy**;

According to the study in Accear [^1], audio clips played by the speakers of a smartphone can be recovered by processing IMU readings, specifically the accelerometer, using a conditional generative adversarial network (cGAN). In this approach, the generator converts accelerometer sequences into spectrograms, while the discriminator evaluates these spectrograms against those from the original audio. Through iterative training, the generator is refined to produce increasingly accurate spectrograms, which can subsequently be converted into sound.
By utilizing the open-source model of Accear, IMU-based sound recovery attacks are launched by *WinSpy*. According to Accear, the Mel-Cepstral Distortion (MCD) is adopted as a key objective indicator for the quality of recovery. Typically, reconstructed audio with MCD below 8dB can be comprehended by a speech recognition system [^2].
In data collection, we generated six digital audio clips, each 4 seconds long and consisting of six spoken numbers. The victim app played these audio clips while the adversary app in multi-window mode records the time-series generated by the accelerometer to launch IMU-based sound recovery attacks. Each audio clip was played 10 times.
We calculated the maximum, minimum, and mean MCD values for each audio clip, as presented in Table. The MCD values range from 5.43dB to 6.78dB on the Magic V2 and from 5.98dB to 8.9dB on the P30, meeting the requirements for intelligibility by speech recognition systems as noted. Therefore, we can confirm the efficacy of *WinSpy* in launching IMU-based sound recovery attacks, highlighting the significant risk of playing audio clips in multi-window mode.

| Audio Clip | Device  | MCD-Min | MCD-Mean | MCD-Max |
|------------|---------|---------|----------|---------|
| 314159     | Magic V2| 5.51    | 5.95     | 6.68    |
| 476149     | Magic V2| 5.44    | 6.01     | 6.78    |
| 704288     | Magic V2| 5.43    | 5.83     | 6.72    |
| 895331     | Magic V2| 5.44    | 6.02     | 6.74    |
| 923424     | Magic V2| 5.47    | 6.01     | 6.65    |
| 951413     | Magic V2| 5.54    | 6.05     | 6.64    |
| 314159     | P30     | 5.98    | 7.41     | 8.44    |
| 476149     | P30     | 6.90    | 7.76     | 8.90    |
| 704288     | P30     | 6.80    | 7.82     | 8.60    |
| 895331     | P30     | 6.64    | 7.80     | 8.77    |
| 923424     | P30     | 6.85    | 7.80     | 8.52    |
| 951413     | P30     | 7.06    | 7.75     | 8.51    |


[^1]: Hu, Pengfei, et al. "Accear: Accelerometer acoustic eavesdropping with unconstrained vocabulary." 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2022.
[^2]: Yan, Chen, et al. "The feasibility of injecting inaudible voice commands to voice assistants." IEEE Transactions on Dependable and Secure Computing 18.3 (2019): 1108-1124.

