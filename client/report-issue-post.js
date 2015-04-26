$("#report-issue-form").submit(function(e)
{
    e.preventDefault(); //STOP default action
    var postData = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data : postData,
        success: function(data, textStatus, jqXHR)
        {
            window.r = data
            if (data.status == "success")
            {
                alert('Thanks for the report')
            }
            else
            {
                alert('There was a problem with the data your provided')
            }
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('Oops, something went wrong')
        }
    });
    e.unbind(); //unbind. to stop multiple form submit.
});
