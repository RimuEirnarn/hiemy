import './jquery.js'

function isValidUrl(str) {
    const pattern = new RegExp(
        '^([a-zA-Z]+:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR IP (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
        '(\\#[-a-z\\d_]*)?$', // fragment locator
        'i'
    );
    return pattern.test(str);
}


var sanitizeHTML = function (str) {
    return str.replace(/[^\w. ]/gi, function (c) {
        return '&#' + c.charCodeAt(0) + ';';
    });
};

function validate() {
    let target = $("#url")
    let data = target.val()
    if (!isValidUrl(data)) {
        target.addClass("is-invalid")
        target.parent().addClass("is-invalid")
        throw new Error("URL Invalid")
    }
    if (target.hasClass('is-invalid')) {
        target.parent().removeClass('is-invalid')
        target.removeClass('is-invalid')
    }
    return data
}

function shorten() {
    $("#messages").empty()
    let target = validate()
    if (target === undefined) return
    $.ajax({
        data: {
            target
        },
        url: "/url/",
        success(resp) {
            let status = resp['status']
            let message = resp['message']
            console.log(`${status} -> ${message}`)
            createFlash(status, message)
            show(resp['url'])
        },
        statusCode: {
            400: (resp) => {
                // console.log(resp, resp.responseJSON)
                let json = resp.responseJSON
                let status = json['status']
                let message = json['message']
                console.log(`${status} -> ${message}`)
                createFlash(status, String(message))
            }
        },
        method: "POST"
    })
}

function show(url) {
    $("#result").show()
    let result = $("#result-target")
    result.attr("href", url)
    result.text(url)
}

function createFlash(category, message) {
    let cat = sanitizeHTML(category)
    if (!["error", "success", "warning"].includes(cat)) {
        createFlash('error', "E-INVFLASH")
        console.error(`Cannot create flash, ${cat} is undefined`)
        return
    }
    let mes = sanitizeHTML(message)
    let icon = ""
    let type = cat
    switch (type) {
        case "error":
            icon = '<i class="bi bi-x-circle-fill"></i>'
            break;
        case "success":
            icon = '<i class="bi bi-check-circle-fill"></i>'
            break
        case "warning":
            icon = '<i class="bi bi-exclamation-circle-fill"></i>'
            break
        default:
            break;
    }
    if (type == 'error') type = "danger"
    $("#messages").append(`<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${icon}
  <strong>${cat}</strong> ${mes}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
    `)
}


jQuery(() => {
    console.log("Initialised")
    createFlash('success', "app initialised")
    $("#push").on("click", (event) => shorten())
    $("#result").hide()
    $(document).on('keypress', (event) => {
        console.log(event.key)
        if (event.key == "Enter") return shorten()
    })
})
