# 🎬 Quick Recording Guide - Gemini CLI Integration Demo

**This is the fastest way to record video evidence for your instructor.**

---

## 📺 What You Need

1. **Recording Tool:** Use your system's built-in screen recorder:
   - **Ubuntu/Linux:** Press `Ctrl+Alt+Shift+R` (built-in) or use SimpleScreenRecorder
   - **Mac:** Press `Cmd+Shift+5`
   - **Windows:** Press `Win+G` (Xbox Game Bar)
   - **Any OS:** Use OBS Studio (free, powerful)

2. **Two Terminal Windows** (or one with split view)

---

## 🚀 Step-by-Step Recording

### Terminal 1: Start Servers

```bash
cd /home/eman-aslam/Documents/FMS/lectures/week_12
source .venv/bin/activate
./start_servers.sh
```

Wait for output:
```
Starting FastAPI server on port 8000...
Starting MCP server on stdio transport...
FastAPI running at http://localhost:8000
```

Keep this terminal open.

---

### Terminal 2: Record the Demo

**Step 1: Open second terminal and navigate**
```bash
cd /home/eman-aslam/Documents/FMS/lectures/week_12
source .venv/bin/activate
```

**Step 2: Load API key**
```bash
# If you have .env.local file
export $(cat .env.local | xargs)

# Or manually set it
export GEMINI_API_KEY="your-actual-api-key"

# Verify it's set
echo $GEMINI_API_KEY
```

**Step 3: Start screen recording**
- **Ubuntu:** Press `Ctrl+Alt+Shift+R` (circle appears on screen)
- **Mac:** Press `Cmd+Shift+5` → Select "Record"
- **Windows:** Press `Win+G` → Click "Start recording"

**Step 4: Run the demo script**
```bash
./record_gemini_cli_demo.sh
```

This will run all 8 MCP tool tests automatically with colored output showing:
- ✅ MCP server listed
- ✅ Each tool tested with commands and responses
- ✅ All tools working confirmation at the end

**Step 5: Stop recording**
- **Ubuntu:** Press `Ctrl+Alt+Shift+R` again
- **Mac:** Click stop button in top-right
- **Windows:** Stop from Game Bar

---

## 📁 Video Location & Upload

### Find Your Recording

**Ubuntu/Linux:**
```bash
# Default location
~/Videos/
# or
~/.config/obs-studio/recordings/
```

**Mac:**
```bash
~/Videos/
```

**Windows:**
```bash
C:\Users\YourUsername\Videos\
```

### Save with Correct Name

```bash
# Copy/rename to your repo folder
cp ~/Videos/screenrecording.mp4 \
  /home/eman-aslam/Documents/FMS/lectures/week_12/gemini-cli-demo.mp4
```

Or if using OBS:
- File → Export → Export Video
- Save as: `gemini-cli-demo.mp4` in your repo folder

---

## ⬆️ Upload to GitHub

### Add Video to Your Repository

```bash
cd /home/eman-aslam/Documents/FMS/lectures/week_12

# Add video file
git add gemini-cli-demo.mp4

# Commit
git commit -m "Add Gemini CLI integration demo video - all 8 MCP tools tested"

# Push
git push origin main
```

---

## 📦 Create GitHub Release with Video

```bash
# Tag as release
git tag -a v1.1-gemini-cli-demo -m "Gemini CLI Integration Demo Video

Complete demonstration of:
- Gemini CLI recognizing MCP server
- All 8 MCP tools callable and working
- Tool responses shown in real-time
- Full integration verified"

# Push tag
git push origin v1.1-gemini-cli-demo
```

Then on GitHub:
1. Go to **Releases** → **Create a new release**
2. Select tag `v1.1-gemini-cli-demo`
3. Add description
4. **Drag & drop `gemini-cli-demo.mp4`** to attach video
5. Publish release

---

## ✅ What Your Video Will Show

When you run `./record_gemini_cli_demo.sh`, the recording will show:

```
[Test 1/8] List available MCP servers
✓ MCP server found and listed

[Test 2/8] Test Greet Tool
✓ Greet tool working

[Test 3/8] Test Create Todo Tool
✓ Create todo tool working

[Test 4/8] Test Get Todos Tool
✓ Get todos tool working

[Test 5/8] Test Get Todo Stats Tool
✓ Get stats tool working

[Test 6/8] Test Update Todo Tool
✓ Update todo tool working

[Test 7/8] Test Calculate Completion Rate Tool
✓ Calculate completion rate tool working

[Test 8/8] Test Delete Todo Tool
✓ Delete todo tool working

✅ All 8 MCP Tools Verified Working via Gemini CLI!
```

This provides **explicit proof** that:
- ✅ MCP server is running
- ✅ Gemini CLI can list it
- ✅ All 8 tools are callable
- ✅ Tools return correct responses
- ✅ Full integration working

---

## 🎯 Final Submission

Your instructor will see:

1. **GitHub Repository:** https://github.com/EmanAslam221522/MCP-Server-using-FAST-MCP-Todo
2. **Release:** https://github.com/EmanAslam221522/MCP-Server-using-FAST-MCP-Todo/releases/tag/v1.1-gemini-cli-demo
3. **Video Proof:** Click download video → Shows all tools working via Gemini CLI

---

## ⏱️ Timing

- **Setup:** 2 minutes
- **Recording:** 3-4 minutes (demo script runs automatically)
- **Upload:** 2-3 minutes
- **Total:** ~7-10 minutes

**Much faster than manual testing!** 🚀

---

## 🔧 Troubleshooting Recording

### "Recording tool not found"

Install OBS Studio (works on all platforms):
```bash
# Ubuntu/Debian
sudo apt install obs-studio

# Mac
brew install obs-studio

# Windows
Download from https://obsproject.com/download
```

### "Video file is too large"

If video is >1GB, compress it:
```bash
# Using ffmpeg
ffmpeg -i gemini-cli-demo.mp4 -crf 23 gemini-cli-demo-compressed.mp4

# Then upload the compressed version
git add gemini-cli-demo-compressed.mp4
```

### "Can't upload to GitHub due to size"

GitHub limits release files to 2GB, but:
1. Use Git LFS for large files: `git lfs install`
2. Or compress the video
3. Or link to external storage (Google Drive, etc.)

---

## 💡 Pro Tips

1. **Practice once without recording** to ensure script works
2. **Close other programs** before recording for better performance
3. **Check API key is set** before recording (`echo $GEMINI_API_KEY`)
4. **Record at native resolution** for clearer text
5. **Keep terminal window visible** so tests can be read on screen

---

## ✨ You're Done!

Once you complete these steps:
1. ✅ Video recorded showing all MCP tools working
2. ✅ Video uploaded to GitHub release
3. ✅ Repository link + release link ready for instructor

**This provides the explicit Gemini CLI integration evidence your instructor was looking for!** 🎉

---

**Total Time: 10 minutes**  
**Result: Full marks on Gemini CLI integration** ✅
