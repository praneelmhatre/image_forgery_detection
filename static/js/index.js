import Dropzone from "dropzone";
const dropArea = document.querySelector(".drag-area");
dragText = dropArea.querySelector("h2");
button = dropArea.querySelector("button");
input = dropArea.querySelector("input");

let file;

// If you are using CommonJS modules:
const { Dropzone } = require("dropzone");

// If you are using an older version than Dropzone 6.0.0,
// then you need to disabled the autoDiscover behaviour here:
Dropzone.autoDiscover = false;

let myDropzone = Dropzone({
  paramName: "file", // The name that will be used to transfer the file
  // maxFilesize: 2, // MB
});
button.onclick = () => {
  input.click();
};

input.addEventListener("change", function () {
  file = this.files[0];
  showFile();
  dropArea.classList.add("active");
});

dropArea.addEventListener("dragover", (event) => {
  event.preventDefault();
  console.log("File is over DragArea");
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

dropArea.addEventListener("dragleave", () => {
  console.log("File is over  from DragArea");
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

dropArea.addEventListener("drop", (event) => {
  event.preventDefault();
  console.log("File is dropped on DragArea");
  dropArea.classList.remove("active");
  file = event.dataTransfer.files[0];
  showFile();
});

function showFile() {
  input.click();
  let fileType = file.type;
  console.log(fileType);

  let validExtensions = ["image/png", "image/jpeg", "image/jpg"];
  if (validExtensions.includes(fileType)) {
    let fileReader = new FileReader();
    fileReader.onload = () => {
      let fileURL = fileReader.result;
      console.log(fileURL);
      let imgTag = `<img src="${fileURL}" alt="">`;
      dropArea.innerHTML = imgTag;
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not a valid image file");
    dropArea.classList.remove("active");
  }
}

/**
 * Create an arrow function that will be called when an image is selected.
 */
const previewImage = (event) => {
  /**
   * Get the selected files.
   */
  const imageFiles = event.target.files;
  /**
   * Count the number of files selected.
   */
  const imageFilesLength = imageFiles.length;
  /**
   * If at least one image is selected, then proceed to display the preview.
   */
  if (imageFilesLength > 0) {
    /**
     * Get the image path.
     */
    const imageSrc = URL.createObjectURL(imageFiles[0]);
    /**
     * Select the image preview element.
     */
    const imagePreviewElement = document.querySelector(
      "#preview-selected-image"
    );
    /**
     * Assign the path to the image preview element.
     */
    imagePreviewElement.src = imageSrc;
    /**
     * Show the element by changing the display value to "block".
     */
    imagePreviewElement.style.display = "block";
  }
};
