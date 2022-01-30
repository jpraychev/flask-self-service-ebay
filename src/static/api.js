const removeDisplay = (item) => {
    $(`${item}`).css('display', 'none')
    $('#email-address').val('')
}

const addDisplay = (triggerItem, resultItem, content) => {
    $(`${triggerItem}`).css('display', 'block')
    $(`${resultItem}`).html(content)
}

$('.close').on('click', () => {
    removeDisplay('#myModal');
});

$(window).on('click', (e) => {
    if (e.target.id === 'myModal') {
        removeDisplay('#myModal');
    };
});

$("#email-button").on("click", () => {
    const email_addr = $("#email-address").val()
    if (!email_addr) {
        addDisplay(
                    triggerItem='#myModal',
                    resultItem='#modal-text',
                    content='Email field is empty!')
        return 
    }
    userOnboarding(url='http://127.0.0.1:5000/onboard', email=email_addr);
});

const userOnboarding = async (url, email) => {        
    var myHeaders = new Headers()
    myHeaders.append("Content-Type", "application/json")

    var raw = JSON.stringify({
        "email": email
    })

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    }
    
    try {
        const response = await fetch(url, requestOptions)
        if (response.status === 200) {
            const result = await response.text()
            if (result !== "0") {
                addDisplay(
                    triggerItem='#myModal', 
                    resultItem='#modal-text', 
                    content=`Something went wrong in the backend. Status code ${result}`);
                return
            }
            addDisplay(triggerItem='#myModal', resultItem='#modal-text', content=`${email} has been onboarded`);
        }
    }
    catch (error) {
        console.log(error)
    }
}