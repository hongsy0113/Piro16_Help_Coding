currentURL = window.location.href.split("/")

var redirectURL = "";
const successButton = document.querySelector("#qna-form-success-button");
const cancelButton = document.querySelector("#qna-form-cancel-button");

if (currentURL[currentURL.length - 1] == "update") {

  successButton.innerHTML = "수정";
  for (index = 0; index < currentURL.length - 1; index++) {
    redirectURL = redirectURL + currentURL[index];
    redirectURL = redirectURL + "/";
  }
  cancelButton.href = redirectURL;

}