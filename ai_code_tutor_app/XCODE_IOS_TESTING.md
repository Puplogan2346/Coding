# Testing AI Code Tutor in Xcode / iPhone Simulator

This project is a Python + Streamlit web app, not a native iOS app. Xcode is still useful for previewing the learner experience on an iPhone-sized screen.

## Option A: Fastest iPhone Simulator test

1. Run the Streamlit app on your Mac:

```bash
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

2. Open **Xcode**.
3. Go to **Xcode > Open Developer Tool > Simulator**.
4. In the Simulator, open Safari.
5. Try this address first:

```text
http://localhost:8501
```

If that does not load, use your Mac's local network address instead:

```bash
ipconfig getifaddr en0
```

Then open:

```text
http://YOUR-MAC-IP:8501
```

Example:

```text
http://192.168.1.25:8501
```

## Option B: Simple SwiftUI WebView wrapper

Use this when you want the app to look like a real iPhone app shell while the Streamlit server still runs on your Mac.

1. Open Xcode.
2. Create a new **iOS App** project.
3. Interface: **SwiftUI**.
4. Language: **Swift**.
5. Replace the generated `ContentView.swift` with `ios_wrapper/ContentView.swift`.
6. Replace or compare the generated app entry file with `ios_wrapper/AI_Code_TutorApp.swift`.
7. Add the local-network Info.plist snippet from `ios_wrapper/Info.plist-snippet.xml` if your wrapper cannot load the local HTTP app.
8. Run the Streamlit app locally.
9. Press **Run** in Xcode with an iPhone Simulator selected.

## Important limits

- The WebView wrapper is for testing and private use, not App Store submission.
- The Streamlit app must be running somewhere the iPhone Simulator can reach.
- For a real mobile app later, you would either host the Streamlit app privately and open the hosted URL in the wrapper, or rebuild the experience as a native Swift app that talks to a backend.
- Keep `ALLOW_CODE_RUNNER=false` unless you are testing locally on your own machine.
