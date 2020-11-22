
    $('input[type=radio]').click(function(){
    if (this.previous) {
        this.checked = false;
    }
    this.previous = this.checked;
});
