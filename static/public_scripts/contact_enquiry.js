(function($){
    $('#sendEnquiryBtn').click(function(ev){
        ev.preventDefault();
        
        // call form validation function
       handleFormSubmit();
       
        var serializedData = $('#bsContactForm').serialize();
        var url = $('#bsContactForm').data('url')

        $.ajax({
            type: 'post',
            dataType: 'json',
            url: url,
            data: serializedData,
            success: function(response){
                let container = $('#bs-success-container');

                let myInfo = `<br/><div class="alert alert-info alert-dismissible mb-3 text-center" role="alert"><h6 class="text-capitalize">${response.contact.name}: message sent<span>&#10003;</span></h6><button type="button" class="close" data-dismiss="alert">&times;</button></div>`
                container.append(myInfo);
                var timerId;
                timerId = setTimeout(() =>{
                    container.empty();
                }, 5000)

                clearTimeout(() =>{timerId})
            },
            error: function(response){
                let container = $('#bs-success-container');

                let myInfo = '<br/><div class="alert alert-warning alert-dismissible mb-3 text-center" role="alert"><h6 class="text-capitalize text-danger">message not sent<span>&times;</span></h6><button type="button" class="close" data-dismiss="alert">&times;</button></div>'
                container.append(myInfo);
                var timerId;
                timerId = setTimeout(() =>{
                    container.empty();
                }, 3000)

                clearTimeout(() =>{timerId})
            }
        })
        $('#bsContactForm')[0].reset();
    })
})(jQuery);


// for form validation js
function handleFormSubmit(){
    const form = document.getElementsByTagName('form').value;
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const message = document.getElementById('message').value;
    if (form == ""){
        alert("Please fill in the form below!")
        document.getElementsByTagName('form').style.borderColor = 'red';
        return false;
    }else if (name == ""){
        alert("Please fill in your name!")
        document.getElementById('name').style.borderColor = 'red';
        return false;
    }else if (email == ""){
        alert("Please fill in your email!")
        document.getElementById('email').style.borderColor = 'red';
        return false;
    }else if (phone == ""){
        alert("Please fill in your phone number!")
        document.getElementById('phone').style.borderColor = 'red';
        return false;
    }else if (message == ""){
        alert("Message can not be empty!")
        document.getElementById('message').style.borderColor = 'red';
        return false;
    }else{
        return true
    }
}
