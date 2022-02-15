// qna 게시글 작성과 관련된 js
const addTag = document.querySelector("#add_tag");
addTag.addEventListener("click", create_tag, {once: true});

function create_tag() {
    const inputBox = document.querySelector('.tag_input_box');
    const tagInput = document.createElement('div');
    tagInput.setAttribute('class', 'group-post__form-box');
    tagInput.innerHTML = "<input type='text' placeholder='태그를 입력하세요.' class='input_tag group-post__form-input'/> <input type='button' value='추가' class='add_btn group-post__form-label' />";
    inputBox.appendChild(tagInput);

    const addBtn = document.querySelector(".add_btn");
    addBtn.addEventListener("click", add);
}

function add() {
    // 태그 div
    const tagBox = document.querySelector(".select__tag");
    // 태그 입력창
    const inputTag = document.querySelector(".input_tag");
    // 새로운 태그 추가

    if (inputTag.value.length > 0 && inputTag.value.length < 20) {

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

    // if (inputTag.value) {
    //     newLabel.append(inputTag.value);
    //     tagBox.append(newTag);
    //     tagBox.append(newLabel);
    //     // addTag.style.backgroundColor = color;
    //     inputTag.value = "";
    // }
}



