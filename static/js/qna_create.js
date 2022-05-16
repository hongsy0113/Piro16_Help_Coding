// qna 게시글 작성과 관련된 js
const addTag = document.querySelector("#add_tag");
addTag.addEventListener("click", create_tag, {once: true});

function create_tag() {
    const inputBox = document.querySelector('.tag_input_box');
    const tagInput = document.createElement('form');
    tagInput.setAttribute('class', 'group-post__form-box');
    tagInput.innerHTML = "<input type='text' maxlength='20' placeholder='태그는 20자 이내로 입력하세요.' class='input_tag group-post__form-input'/> <input type='button' value='추가' class='add_btn group-post__form-label' />";
    inputBox.appendChild(tagInput);

    const addBtn = document.querySelector(".add_btn");
    addBtn.addEventListener("click", add);
}

function add() {
    // 태그 div
    const tagBox = document.querySelector(".post-create__tag-select");
    // 태그 입력창
    const inputTag = document.querySelector(".input_tag");
    // 새로운 태그 추가

    if (inputTag.value.length > 0 && inputTag.value.length <= 20) {

        const newTag = document.createElement("input");
        const newLabel = document.createElement("label")
        newTag.setAttribute('type', 'checkbox');
        newTag.setAttribute('name', 'detail_tag');
        newTag.setAttribute('value', inputTag.value);
        newTag.setAttribute('class', 'tag');
        newTag.setAttribute('id', inputTag.value);
        newLabel.setAttribute('for', inputTag.value);

        newLabel.append(inputTag.value);
        tagBox.append(newTag);
        tagBox.append(newLabel);
        // addTag.style.backgroundColor = color;
        inputTag.value = "";
    }
    else{
        const errorElement = document.querySelector(".add_tag__error-msg");
        errorElement.innerHTML = "태그는 20자 이내로 입력해주세요.";
        // alert("태그를 20자 이하로 입력해주세요");
    }
    // const color = "#FFFFF";

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