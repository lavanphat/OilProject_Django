var DashboardConfig = {
    myChart: null,
}
var DasboardController = {
    init: function () {
        DasboardController.today();
        DasboardController.register();
    },
    register: function () {
        $('.kt-subheader__wrapper a').click(function () {
                $('.kt-subheader__wrapper').each(function () {
                    $('.kt-subheader__wrapper a').removeClass().addClass('btn kt-subheader__btn-secondary');
                })
                $(this).addClass('btn kt-subheader__btn-primary');
                var time = $(this).attr('id');
                if (time == 'today') {
                    DasboardController.today();
                    $('.kt-portlet__head-toolbar').fadeIn();
                } else if (time == 'week') {
                    $('#title').text('THỐNG KÊ THEO TUẦN');
                    DasboardController.week();
                    $('.kt-portlet__head-toolbar').fadeOut();
                } else if (time == 'month') {
                    $('#title').text('THỐNG KÊ THEO THÁNG');
                    DasboardController.month();
                    $('.kt-portlet__head-toolbar').fadeIn();
                    $('#kt_datepicker_1_modal').val('');
                    $('#filter-date').off('click').on('click', function () {
                        var jsDate = ($('#kt_datepicker_1_modal').val());
                        var month = (jsDate.substring(3, 5));
                        var year = (jsDate.substring(6, 10));
                        var data = {
                            month: month, year: year,
                        };
                        var url_bill = $('#month').data('url-bill');
                        DasboardController.loadBill(url_bill, data);
                        var url_product = $('#month').data('url-product');
                        DasboardController.loadProduct(url_product, data);
                        var url_service = $('#month').data('url-service');
                        DasboardController.loadService(url_service, data);
                        var url_money = $('#month').data('url-money');
                        DasboardController.loadMoney(url_money, data);
                    });
                } else if (time == 'year') {
                    $('#title').text('THỐNG KÊ THEO NĂM');
                    DasboardController.year();
                    $('.kt-portlet__head-toolbar').fadeOut();
                }
            }
        );
        $('#kt_datepicker_1_modal').datepicker({
            todayHighlight: true,
            format: "dd/mm/yyyy",
        });
        $('#filter-date').off('click').on('click', function () {
            var jsDate = ($('#kt_datepicker_1_modal').val());
            var day = (jsDate.substring(0, 2));
            var month = (jsDate.substring(3, 5));
            var year = (jsDate.substring(6, 10));
            var data = {
                day: day, month: month, year: year,
            };
            var url_bill = $(this).data('url-bill');
            DasboardController.loadBillWithDay(url_bill, data);
            var url_product = $(this).data('url-product');
            DasboardController.loadProductWithDay(url_product, data);
            var url_service = $(this).data('url-service');
            DasboardController.loadServiceWithDay(url_service, data);
            var url_money = $(this).data('url-money');
            DasboardController.loadMoneyWithDay(url_money, data);
        })
    },
    // today
    loadBill: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            data: data,
            url: url,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    var color = ['rgba(255, 99, 132, 1)'];
                    bills.forEach(function () {
                        color.push(DasboardController.getRandomColor())
                    })
                    DasboardController.chartLine(labels, bills, color)
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    loadBillWithDay: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            url: url,
            data: data,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    var color = ['rgba(255, 99, 132, 1)'];
                    bills.forEach(function () {
                        color.push(DasboardController.getRandomColor())
                    })
                    DasboardController.chartLine(labels, bills, color)
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    chartLine: function (labels, bills, color) {
        if (window.bar != undefined) {
            window.bar.destroy();
        }
        var ctx = document.getElementById('bill-day');
        window.bar = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Số Lượng Hóa Đơn',
                    data: bills,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    pointBackgroundColor: color,
                    pointBorderColor: color,
                    borderWidth: 5,
                },
                ]
            },
            options: {
                // responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: 'Hóa Đơn'
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                }
            }
        });
    },

    loadMoney: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            data: data,
            url: url,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    var total = 0;
                    bills.forEach(function (num) {
                        total += parseInt(num);
                    });
                    $('#total').text(KTUtil.numberString(total + ' VND'));
                    if (data.time == 'today') {
                        DasboardController.chartBar(labels, bills,)
                    }
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    loadMoneyWithDay: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            data: data,
            url: url,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    var total = 0;
                    bills.forEach(function (num) {
                        total += parseInt(num);
                    });
                    $('#total').text(KTUtil.numberString(total + ' VND'));
                    if (data.time == 'today') {
                        DasboardController.chartBar(labels, bills)
                    }
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    chartBar: function (labels, bills) {
        if (window.line != undefined) {
            window.line.destroy();
        }
        var ctx = $('#money-day');
        window.line = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Doanh thu',
                    data: bills,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 5,
                },
                ]
            },
            options: {
                // responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: 'Tổng Tiền'
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            var value = data.datasets[0].data[tooltipItem.index];
                            value = value.toString();
                            value = value.split(/(?=(?:...)*$)/);
                            value = value.join(',');
                            return value;
                        }
                    } // end callbacks:
                },

                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            userCallback: function (value, index, values) {
                                // Convert the number to a string and splite the string every 3 charaters from the end
                                value = value.toString();
                                value = value.split(/(?=(?:...)*$)/);
                                value = value.join(',');
                                return value;
                            }
                        }
                    }],
                }
            }
        });
    },

    getRandomColor: function () {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },
    loadProduct: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            url: url,
            data: data,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    if (data.time == 'today') {
                        var color = [];
                        bills.forEach(function () {
                            color.push(DasboardController.getRandomColor())
                        })
                        DasboardController.chartPie(labels, bills, color)
                    }
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    loadProductWithDay: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            data: data,
            url: url,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    if (data.time == 'today') {
                        var color = [];
                        bills.forEach(function () {
                            color.push(DasboardController.getRandomColor())
                        })
                        DasboardController.chartPie(labels, bills, color)
                    }
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    chartPie: function (labels, bills, color) {
        if (window.pie != undefined) {
            window.pie.destroy();
        }
        var ctx = document.getElementById('product-day');
        window.pie = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [
                    {
                        labels: 'Points',
                        backgroundColor: color,
                        data: bills,
                    }
                ]
            },
            options: {
                // responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: 'Sản phẩm đã bán'
                }
            }
        })
    },

    loadService: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            url: url,
            data: data,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    if (data.time == 'today') {
                        var color = [];
                        bills.forEach(function () {
                            color.push(DasboardController.getRandomColor())
                        })
                        DasboardController.chartPolarArea(labels, bills, color)
                    }
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    loadServiceWithDay: function (url, data) {
        var labels = []
        var bills = []
        $.ajax({
            type: 'get',
            url: url,
            data: data,
            success: function (data) {
                if (data.status == true) {
                    labels = data.labels;
                    bills = data.data;
                    if (data.time == 'today') {
                        var color = [];
                        bills.forEach(function () {
                            color.push(DasboardController.getRandomColor())
                        })
                        DasboardController.chartPolarArea(labels, bills, color)
                    }
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    },
    chartPolarArea: function (labels, bills, color) {
        if (window.polar != undefined) {
            window.polar.destroy();
        }
        var ctx = $('#service-day');
        window.polar = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: labels,
                datasets: [
                    {
                        labels: 'Points',
                        backgroundColor: color,
                        data: bills,
                    }
                ]
            },
            options: {
                // responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: 'Dịch vụ đã bán'
                }
            }
        })
    },

    //today
    today: function () {
        var url_bill = $('#today').data('url-bill');
        DasboardController.loadBill(url_bill);
        var url_product = $('#today').data('url-product');
        DasboardController.loadProduct(url_product);
        var url_service = $('#today').data('url-service');
        DasboardController.loadService(url_service);
        var url_money = $('#today').data('url-money');
        DasboardController.loadMoney(url_money);
    },

    // week
    week: function () {
        var url_bill = $('#week').data('url-bill');
        DasboardController.loadBill(url_bill)
        var url_product = $('#week').data('url-product');
        DasboardController.loadProduct(url_product)
        var url_service = $('#week').data('url-service');
        DasboardController.loadService(url_service)
        var url_money = $('#week').data('url-money');
        DasboardController.loadMoney(url_money)
    },

    //month
    month: function () {
        var url_bill = $('#month').data('url-bill');
        DasboardController.loadBill(url_bill);
        var url_product = $('#month').data('url-product');
        DasboardController.loadProduct(url_product);
        var url_service = $('#month').data('url-service');
        DasboardController.loadService(url_service);
        var url_money = $('#month').data('url-money');
        DasboardController.loadMoney(url_money);
    },

    //year
    year: function () {
        var url_bill = $('#year').data('url-bill');
        DasboardController.loadBill(url_bill);
        var url_product = $('#year').data('url-product');
        DasboardController.loadProduct(url_product);
        var url_service = $('#year').data('url-service');
        DasboardController.loadService(url_service);
        var url_money = $('#year').data('url-money');
        DasboardController.loadMoney(url_money);
    }
}
DasboardController.init()