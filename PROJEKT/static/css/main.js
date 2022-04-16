function myFunction(selectObject, idInputu) {
    const value = selectObject.value;
    const input = document.getElementById("input_"+idInputu);
    console.log(input);
    input.value = value;
}
function myFunction2(selectObject, idInputu) {
    const value = selectObject.value;
    const input = document.getElementById("input2_"+idInputu);
    input.value = value;
}
