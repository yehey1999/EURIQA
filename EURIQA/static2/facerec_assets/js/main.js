const video = document.getElementById('video')
const MODEL_URL = '/static2/facerec_assets/models'

// Calling all models from the models folder
Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
  faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL),
]).then(startVideo)

// Function that initiates the video
function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

video.addEventListener('play', () => {
  // Declare unknown face counter
  var unknownCtr=0;

  // Create the canvas where the bounding box will be shown
  const canvas = faceapi.createCanvasFromMedia(video)
  document.getElementById("video_area").append(canvas)
  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)

  let labeledFaceDescriptors
  (async () => {
    labeledFaceDescriptors = await loadLabeledImages()
  })()

  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)

    if (labeledFaceDescriptors) {
      const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6)
      const results = resizedDetections.map(d => faceMatcher.findBestMatch(d.descriptor))

      // Draw the bounding box based on the results
      results.forEach((result, i) => {
        const box = resizedDetections[i].detection.box
        const drawBox = new faceapi.draw.DrawBox(box, { label: result.toString() })
        drawBox.draw(canvas)

        // Count the times the detected face is unknown
        const stringresult = result.toString().split(" ");
        if (stringresult[0] == "unknown"){
          unknownCtr++;
        }
      })
    }

  }, 200)
})

// Function that checks and loads the images
function loadLabeledImages() {
  const labels = ['emma']
  return Promise.all(
    labels.map(async label => {
      const descriptions = []
      for (let i = 1; i <= 1; i++) {
        const img = await faceapi.fetchImage(`/static2/facerec_assets/images/${label}.png`)
        const detections = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor()
        descriptions.push(detections.descriptor)
      }
      
      return new faceapi.LabeledFaceDescriptors(label, descriptions)
    })
  )
}