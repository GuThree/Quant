$(function () {
    $("#start_date").datetimepicker({
        format: 'yyyy-mm-dd ',
        startDate: '0',
        language: "zh-CN",
        autoclose: true,
        minView: "month",   //不显示时分秒
        todayHighlight: true,   //当天高亮显示
    });
});
$(function () {
    $("#end_date").datetimepicker({
        format: 'yyyy-mm-dd ',
        startDate: '0',
        language: "zh-CN",
        autoclose: true,
        minView: "month",   //不显示时分秒
        todayHighlight: true,   //当天高亮显示
    });
});
