$("#btnBuscar").click(function () {
    debugger;
    $.blockUI({ message: null });
    var id = $("#ddlEmpresa").val().split('|'); ;
    var pCodigoEmpresa = id[1];
    var servicio = ($("#ddlOrigen :selected").text() + " A " + $("#ddlDestino :selected").text());
    window.location.href = "Datos.aspx?pCodigoEmpresa=" + pCodigoEmpresa + "&pCodigoLinea=" + $("#ddlLinea").val() + "&pCodigoOrigen=" + $("#ddlOrigen").val() + "&pCodigoDestino=" + $("#ddlDestino").val() + "&pServicio=" + servicio + "&pCodigoParada=" + $("#ddlParada").val() + "&pProveedor=yv";
});

// otras consultas a empresas con ramales
$("#btnBuscarCY").click(function () {
    $.blockUI({ message: null });
    var id = $("#ddlEmpresa").val().split('|'); ;
    var pCodigoEmpresa = id[1];
    var servicio = ($("#ddlRamal :selected").text());
    window.location.href = "Datos.aspx?pCodigoEmpresa=" + pCodigoEmpresa + "&pCodigoRamal=" + $("#ddlRamal").val() + "&pServicio=" + servicio + "&pCodigoParada=" + $("#ddlParadaCY").val() + "&pProveedor=cy";
});