const inputImage = document.querySelector("#image");
const inputFile = document.querySelector("#attached_file");

inputImage.addEventListener("change", inputImageMessage);
inputFile.addEventListener("change", inputFileMessage);

function inputImageMessage() {
    const fileName = inputImage.value;
    const uploadImageName = document.querySelector(".group-post__form-input--image");
    uploadImageName.value = fileName;
}

function inputFileMessage() {
    const fileName = inputFile.value;
    const uploadFileName = document.querySelector(".group-post__form-input--file");
    uploadFileName.value = fileName;
}

