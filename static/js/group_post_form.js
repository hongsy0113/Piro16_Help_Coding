const inputImage = document.querySelector("#image");
const inputFile = document.querySelector("#attached_file");

// if (inputImage){inputImage.addEventListener("change", inputImageMessage);}
// if(inputFile){inputFile.addEventListener("change", inputFileMessage);}



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

function imageLoad() {
    const imageRecent = document.querySelector('#img_recent');
    const imageDisplay = document.querySelector('#img_display');
    if (imageRecent.value != "None" && imageRecent.value != "") {
      const imageUploadName = document.querySelector('#img_upload_name');
      imageUploadName.value = String(imageRecent.value);
      const tempImageLocation = document.querySelector('#temp_img_location');
      imageDisplay.hidden = false;
      imageDisplay.src = String(tempImageLocation.value) + String(imageRecent.value);
    } else {
      imageDisplay.hidden = true;
    }
  }
  
function imageChange(event) {
    const imageUpload = document.querySelector('#img_upload');
    const imageUploadName = document.querySelector('#img_upload_name');
    imageUploadName.value = String(imageUpload.value.split('\\').reverse()[0]);
    const imageRecent = document.querySelector('#img_recent');
    imageRecent.value = String(imageUpload.value.split('\\').reverse()[0]);
    
    const imageDisplay = document.querySelector('#img_display');
    imageDisplay.hidden = false;
    imageDisplay.src = URL.createObjectURL(event.target.files[0]);
}
  

function fileLoad() {
    const fileRecent = document.querySelector('#file_recent');
    if (fileRecent.value != "None" && fileRecent.value != "") {
        const fileUploadName = document.querySelector('#file_upload_name');
        fileUploadName.value =  String(fileRecent.value);
        
    }
}
  
function fileChange(event) {
    const fileUpload = document.querySelector('#file_upload');
    const fileUploadName = document.querySelector('#file_upload_name');
    fileUploadName.value =  String(fileUpload.value.split('\\').reverse()[0]);
    const fileRecent = document.querySelector('#file_recent');
    fileRecent.value = String(fileUpload.value.split('\\').reverse()[0]);
    
    const fileDisplay = document.querySelector('#file_display');
    fileDisplay.hidden = false;
    fileDisplay.src = URL.createObjectURL(event.target.files[0]);
}

imageLoad();
fileLoad();



/// 첨부 취소 관련 함수

// 이미지 첨부 취소 버튼
const imgCancel = document.querySelector(".group-post__form-imgcancel");
// 해당 이미지 file input 태그
const imgFile = document.querySelector("#img_upload");

imgCancel.addEventListener('click', function(){
    imgFile.value = null;
    const imageDisplay = document.querySelector('#img_display');
    imageDisplay.hidden = true;
    const imageUploadName = document.querySelector('#img_upload_name');
    imageUploadName.value = null;
    const imageRecent = document.querySelector('#img_recent');
    imageRecent.value = null;

    // 취소 버튼 안 보이게 하기
    imgCancel.hidden = true;
})

// 파일 첨부 취소 버튼
const fileCancel = document.querySelector(".group-post__form-filecancel");
// 해당 파일 file input 태그
const fileFile = document.querySelector("#file_upload");

fileCancel.addEventListener('click', function(){
    fileFile.value = null;
    const fileRecent = document.querySelector('#file_recent');
    fileRecent.value = null;
    const fileUploadName = document.querySelector('#file_upload_name');
    fileUploadName.value = null;

    // 취소 버튼 안 보이게 하기
    fileCancel.hidden = true;
})


// input 태그에 파일 업로드 될 때만 취서 버튼 활성화

const imageUploadName = document.querySelector('#img_upload_name');
const fileUploadName = document.querySelector('#file_upload_name');

imgFile.addEventListener('change', function(){
    if (imgFile.value == null) {
        imgCancel.hidden = true;
    }
    else {
        imgCancel.hidden = false;
    }
})

fileFile.addEventListener('change', function(){
    if (fileFile.value == null) {
        fileCancel.hidden = true;
    }
    else {
        fileCancel.hidden = false;
    }
})