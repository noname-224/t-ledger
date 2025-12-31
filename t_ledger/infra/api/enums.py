from enum import StrEnum


class Method(StrEnum):
    GET = "GET"
    POST = "POST"


class Endpoint(StrEnum):
    GET_ACCOUNTS = "/tinkoff.public.invest.api.contract.v1.UsersService/GetAccounts"
    GET_OPERATIONS = "/tinkoff.public.invest.api.contract.v1.OperationsService/GetOperations"
    GET_OPERATIONS_BY_CURSOR = \
        "/tinkoff.public.invest.api.contract.v1.OperationsService/GetOperationsByCursor"
    GET_PORTFOLIO = "/tinkoff.public.invest.api.contract.v1.OperationsService/GetPortfolio"
    GET_BOND_BY = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/BondBy"
    GET_BOND_COUPONS = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/GetBondCoupons"
