
const chart = echarts.init(document.querySelector('#main'));

// 網頁渲染成功後顯示
$(document).ready(() => {
    drawPM25();
});

function drawPM25() {
    $.ajax(
        {
            url: "/pm25-data",
            type: "POST",
            dataType: "json",
            success: (data) => {
                console.log(data);
                let option = {
                    title: {
                        text: 'PM2.5資料'
                    },
                    tooltip: {},
                    legend: {
                        data: ['數值']
                    },
                    xAxis: {
                        data: data['site']
                    },
                    yAxis: {},
                    series: [
                        {
                            name: '數值',
                            type: 'bar',
                            data: data['pm25']
                        }
                    ]
                };
                chart.setOption(option);

            },
            error: () => {
                alert("取得資料失敗")
            }
        }
    );
}



