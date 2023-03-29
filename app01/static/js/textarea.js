var codeInput = document.getElementById("code-input");
var lineNumber = codeInput.getAttribute("data-line");
var lineNumberDiv = document.createElement("div");
lineNumberDiv.innerHTML = lineNumber;
lineNumberDiv.classList.add("code-line-numbers");
codeInput.parentNode.insertBefore(lineNumberDiv, codeInput);
window.onload = function(){
    codeInput.dispatchEvent(new Event('input'));
}
codeInput.addEventListener("input", function () {
    var lines = this.value.split("\n");
    lineNumberDiv.style.height =  630 + 'px';
    var lineNumbers = "";
    for (var i = 1; i <= lines.length; i++) {
        lineNumbers += i + "<br>";
    }
    lineNumberDiv.innerHTML = lineNumbers;
});

codeInput.addEventListener("scroll", function () {
    lineNumberDiv.scrollTop = this.scrollTop;
});

codeInput.addEventListener("input", function () {
//...其他处理
Prism.highlightAll();
});

// var codeInput = document.getElementById("code-input");
// var lineNumber = codeInput.getAttribute("data-line");
// var lineNumberDiv = document.createElement("div");
// lineNumberDiv.innerHTML = lineNumber;
// lineNumberDiv.classList.add("code-line-numbers");
// codeInput.parentNode.insertBefore(lineNumberDiv, codeInput);
// window.onload = function(){
//     codeInput.dispatchEvent(new Event('input'));
// }
// codeInput.addEventListener("input", function () {
//     var lines = this.value.split("\n");
//     lineNumberDiv.style.height = this.scrollHeight + 'px';
//     lineNumberDiv.style.width = '30px';
//     lineNumberDiv.style.textAlign = 'right';
//     var lineNumbers = "";
//     for (var i = 1; i <= lines.length; i++) {
//         lineNumbers += i + "<br>";
//     }
//     lineNumberDiv.innerHTML = lineNumbers;
// });
//
// codeInput.addEventListener("scroll", function () {
//     lineNumberDiv.scrollTop = this.scrollTop;
// });
//
// codeInput.addEventListener("input", function () {
// //...其他处理
// Prism.highlightAll;
// });
