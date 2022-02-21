const redirectButton = document.querySelector("#profile-redirect");
currentURL = window.location.href.split("/")
if ((currentURL[currentURL.length - 4] != "mypage" || currentURL[currentURL.length - 3] != "reward")
  && currentURL[currentURL.length - 3] != "mypage") {
  redirectButton.innerHTML = "유저페이지로 돌아가기";
  const goQnaButton = document.querySelector("#profile-go-qna");
  if (goQnaButton != null) {
    goQnaButton.remove();
  }
  var redirectURL = "";
  for (index = 0; index < currentURL.length - 2; index++) {
    redirectURL = redirectURL + currentURL[index];
    redirectURL = redirectURL + "/";
  }
  redirectButton.href = redirectURL;
}