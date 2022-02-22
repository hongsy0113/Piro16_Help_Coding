currentURL = window.location.href.split("/")

var redirectURL = "";
const successButton = document.querySelector("#group-form-success-button");
const cancelButton = document.querySelector("#group-form-cancel-button");

if (currentURL[currentURL.length - 2] == "group_create") {

  successButton.innerHTML = "만들기";

} else if (currentURL[currentURL.length - 2] == "group_update") {

  successButton.innerHTML = "수정";
  for (index = 0; index < currentURL.length - 2; index++) {
    redirectURL = redirectURL + currentURL[index];
    redirectURL = redirectURL + "/";
  }
  redirectURL = redirectURL + "group_detail/";
  cancelButton.href = redirectURL;

} else if (currentURL[currentURL.length - 2] == "post_update") {

  successButton.innerHTML = "수정";
  for (index = 0; index < currentURL.length - 2; index++) {
    redirectURL = redirectURL + currentURL[index];
    redirectURL = redirectURL + "/";
  }
  redirectURL = redirectURL + "post_detail/";
  redirectURL = redirectURL + currentURL[currentURL.length - 1];
  cancelButton.href = redirectURL;

}