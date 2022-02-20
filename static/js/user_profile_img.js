function imageLoad() {
  const imageRecent = document.querySelector('#img_recent');
  const imageDisplay = document.querySelector('#img_display');
  if (imageRecent.value != "None" && imageRecent.value != "") {
    const imageUploadName = document.querySelector('#img_upload_name');
    imageUploadName.innerHTML = '선택된 이미지: ' + String(imageRecent.value);
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
  imageUploadName.innerHTML = '선택된 이미지: ' + String(imageUpload.value.split('\\').reverse()[0]);
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

function passwordLoad() {
  const passwordChangeRecent1 = document.querySelector('#password_change_recent_1');
  const passwordChangeRecent2 = document.querySelector('#password_change_recent_2');
  const passwordChangeRecent3 = document.querySelector('#password_change_recent_3');
  const passwordChangeBlock = document.querySelector('#password_change_block');
  if ((passwordChangeRecent1.value != "None" && passwordChangeRecent1.value != "") ||
  (passwordChangeRecent2.value != "None" && passwordChangeRecent2.value != "") ||
  (passwordChangeRecent3.value != "None" && passwordChangeRecent3.value != "")) {
    passwordChangeBlock.hidden = false;
  } else {
    passwordChangeBlock.hidden = true;
  }
}

function passwordChange() {
  const passwordChangeBlock = document.querySelector('#password_change_block');
  if (passwordChangeBlock.style.display == 'none') {
    passwordChangeBlock.style.display = 'flex';
  } else {
    passwordChangeBlock.style.display = 'none';
    document.querySelector('#current_password').value = "";
    document.querySelector('#new_password1').value = "";
    document.querySelector('#new_password2').value = "";
  }
}

console.log("ffff");
imageLoad();
try {
  passwordLoad();
} catch (error) {
  // Do nothing (function only for profile revise)
}
