
    $(document).ready(function () {
        $("#ddlEmpresa").change(function () {
            $.blockUI({ message: null });
            var empresa = $("#ddlEmpresa :selected").text();
            $("#ddlOrigen").html("");
            $("#ddlOrigen").append($("<option></option>").attr("value", "").text("Seleccione su ubicación"))
            $("#ddlOrigen").next(".holderS").text("Seleccione su ubicación");
            $("#ddlDestino").html("");
            $("#ddlDestino").append($("<option></option>").attr("value", "").text("Seleccione su destino"))
            $("#ddlDestino").next(".holderS").text("Seleccione su destino");

            $("#ddlParada").html("");
            $("#ddlParada").append($("<option></option>").attr("value", "").text("Seleccione su parada"))
            $("#ddlParada").next(".holderS").text("Seleccione su parada");

            $("#ddlRamal").html("");
            //            $("#ddlRamal").append($("<option></option>").attr("value", "").text("Seleccione su origen y destino"))
            //            $("#ddlRamal").next(".holderS").text("Seleccione su origen y destino");

            $("#ddlRamal").append($("<option></option>").attr("value", "").text("Seleccione localidad"))
            $("#ddlRamal").next(".holderS").text("Seleccione localidad");

            $("#ddlParadaCY").html("");
            $("#ddlParadaCY").append($("<option></option>").attr("value", "").text("Seleccione su parada"))
            $("#ddlParadaCY").next(".holderS").text("Seleccione su parada");

            if (empresa == "Seleccione una empresa") {
                $("#divYaviene").css("display", "none");
                $("#divColectivoYa").css("display", "none");
                $("#divYV2").css("display", "none");
                $("#divYV3").css("display", "none");
                $("#divYV4").css("display", "none");
                $("#divYV5").css("display", "none");
                $("#btnBuscar").css("display", "none");
                $("#divCY2").css("display", "none");
                $("#divCY3").css("display", "none");
                $("#btnBuscarCY").css("display", "none");
                $("#ddlLinea").html("");
                $("#ddlLinea").append($("<option></option>").attr("value", "").text("Seleccione una linea"))
                $("#ddlLinea").next(".holderS").text("Seleccione una linea");
                $("#ddlRamal").html("");
                //                $("#ddlRamal").append($("<option></option>").attr("value", "").text("Seleccione su origen y destino"))
                //                $("#ddlRamal").next(".holderS").text("Seleccione su origen y destino");
                $("#ddlRamal").append($("<option></option>").attr("value", "").text("Seleccione localidad"))
                $("#ddlRamal").next(".holderS").text("Seleccione localidad");

                $.unblockUI();
            }
            else {
                var params = new Object();
                var id = $("#ddlEmpresa").val().split('|'); ;
                params.pCodigoEmpresa = id[1];
                if (id[0] == 'yv') {
                    $("#divYaviene").css("display", "block");
                    $("#divColectivoYa").css("display", "none");
                    if (id[2] == 1) {
                        params = JSON.stringify(params);
                        $.ajax({
                            type: "POST",
                            url: "MiBondi.asmx/GetLineas",
                            data: params,
                            contentType: "application/json; charset=utf-8",
                            dataType: "json",
                            async: true,
                            success: LoadLineas,
                            error: function (XMLHttpRequest, textStatus, errorThrown) {
                                $.unblockUI();
                                alert(errorThrown);
                            }
                        });
                    }
                    else {
                        params.pCodigoLinea = 0;
                        params = JSON.stringify(params);
                        $.ajax({
                            type: "POST",
                            url: "MiBondi.asmx/GetOrigen",
                            data: params,
                            contentType: "application/json; charset=utf-8",
                            dataType: "json",
                            async: true,
                            success: LoadOrigen,
                            error: function (XMLHttpRequest, textStatus, errorThrown) {
                                $.unblockUI();
                                alert(errorThrown);
                            }
                        });
                    }
                }
                else {
                    $("#divYaviene").css("display", "none");
                    $("#divColectivoYa").css("display", "block");
                    params = JSON.stringify(params);
                    debugger;
                    $.ajax({
                        type: "POST",
                        url: "MiBondi.asmx/GetRamal",
                        data: params,
                        contentType: "application/json; charset=utf-8",
                        dataType: "json",
                        async: true,
                        success: LoadRamal,
                        error: function (XMLHttpRequest, textStatus, errorThrown) {
                            $.unblockUI();
                            alert(errorThrown);
                        }
                    });
                }
            }
        });

        function LoadLineas(result) {
            $("#ddlLinea").html("");
            $("#ddlLinea").append($("<option></option>").attr("value", "").text("Seleccione una linea"));
            $.each(result.d, function () {
                $("#ddlLinea").append($("<option></option>").attr("value", this.codigo).text(this.nombre))
            });
            $("#divYV2").css("display", "block");
            $.unblockUI();
            //                HideError();
        }

        function LoadRamal(result) {
            $("#ddlRamal").html("");
            //            $("#ddlRamal").append($("<option></option>").attr("value", "").text("Seleccione su origen y destino"));
            $("#ddlRamal").append($("<option></option>").attr("value", "").text("Seleccione localidad"));
            $.each(result.d, function () {
                $("#ddlRamal").append($("<option></option>").attr("value", this.codigo).text(this.nombre))
            });
            $("#divCY2").css("display", "block");
            $.unblockUI();
            //                HideError();
        }

        function LoadOrigen(result) {
            $("#ddlOrigen").html("");
            $("#ddlOrigen").append($("<option></option>").attr("value", "").text("Seleccione su ubicación"));
            $.each(result.d, function () {
                $("#ddlOrigen").append($("<option></option>").attr("value", this.codigo).text(this.nombre))
            });
            $("#divYV3").css("display", "block");
            $.unblockUI();
            //                HideError();
        }

    });