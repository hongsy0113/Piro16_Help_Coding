function imageLoad() {
  const imageRecent = document.querySelector('#img_recent');
  if (imageRecent.value != "None" && imageRecent.value != "") {
    const imageUploadName = document.querySelector('#img_upload_name');
    imageUploadName.innerHTML = '선택된 이미지 : ' + String(imageRecent.value);
  }
}

function imageChange() {
  const imageUpload = document.querySelector('#img_upload');
  const imageUploadName = document.querySelector('#img_upload_name');
  imageUploadName.innerHTML = '선택된 이미지 : ' + String(imageUpload.value.split('\\').reverse()[0]);
  const imageRecent = document.querySelector('#img_recent');
  imageRecent.value = String(imageUpload.value.split('\\').reverse()[0]);
  const imageButton = document.querySelector('#img_setting_own');
  imageButton.checked = true;
}

imageLoad();