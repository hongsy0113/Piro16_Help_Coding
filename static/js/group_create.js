function imageLoad() {
    const imageRecent = document.querySelector('#img_recent');
    const imageDisplay = document.querySelector('#img_display');
    if (imageRecent.value != "None" && imageRecent.value != "") {
      const imageUploadName = document.querySelector('#img_upload_name');
      imageUploadName.innerHTML = String(imageRecent.value);
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
    imageUploadName.innerHTML = String(imageUpload.value.split('\\').reverse()[0]);
    const imageRecent = document.querySelector('#img_recent');
    imageRecent.value = String(imageUpload.value.split('\\').reverse()[0]);
    try {
      const imageButton = document.querySelector('#img_setting_own');
      imageButton.checked = true;
    } catch (e) {
    }
    const imageDisplay = document.querySelector('#img_display');
    imageDisplay.hidden = false;
    imageDisplay.src = URL.createObjectURL(event.target.files[0]);
  }
  
imageLoad();
