const dropArea = document.querySelector(".drag-area");
dragText = dropArea.querySelector("h2");
button = dropArea.querySelector("button");
input = dropArea.querySelector("input");

let file;

button.onclick = () =>{
    input.click();
}

input.addEventListener("change",function(){
    file = this.files[0];
    showFile();
    dropArea.classList.add("active");
});

dropArea.addEventListener("dragover", (event)=>{
    event.preventDefault();
    console.log("File is over DragArea")
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File"
})

dropArea.addEventListener("dragleave", ()=>{
    console.log("File is over  from DragArea")
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File"
})

dropArea.addEventListener("drop", (event)=>{
    event.preventDefault();
    console.log("File is dropped on DragArea")
    dropArea.classList.remove("active");
    file = event.dataTransfer.files[0]
    showFile();
});

function showFile(){
    let fileType = file.type;
    console.log(fileType);

    let validExtensions = ["image/png","image/jpeg","image/jpg"];
    if(validExtensions.includes(fileType)){
        let fileReader = new FileReader();
        fileReader.onload = () => {
            let fileURL = fileReader.result;
            console.log(fileURL);
            let imgTag = `<img src="${fileURL}" alt="">`
            dropArea.innerHTML = imgTag;
        }
        fileReader.readAsDataURL(file)
    }
    else{
        alert("This is not a valid image file");
        dropArea.classList.remove("active")
    }
}

