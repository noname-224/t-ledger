from t_ledger.constants import AssetCategory
from t_ledger.domain.dtos import PortfolioDTO
from t_ledger.domain.entities import (
    Portfolio,
    Money,
    AmountByCategory,
    Position,
    Quantity,
)


class PortfolioMapper:

    @staticmethod
    def to_domain(portfolio: PortfolioDTO) -> Portfolio:
        total_amount = Money(
            amount=portfolio.total_amount_portfolio.as_decimal,
            currency=portfolio.total_amount_portfolio.currency,
        )

        amounts_by_category: list[AmountByCategory] = []
        for amount_by_cat in portfolio.amounts_by_category:
            amounts_by_category.append(
                AmountByCategory(
                    category=AssetCategory(amount_by_cat.category),
                    amount=Money(
                        amount=amount_by_cat.amount.as_decimal,
                        currency=amount_by_cat.amount.currency,
                    ),
                ),
            )

        positions: list[Position] = []
        for pos in portfolio.positions:
            positions.append(
                Position(
                    uid=pos.position_uid,
                    instrument_uid=pos.instrument_uid,
                    instrument_type=pos.instrument_type,
                    quantity=Quantity(value=pos.quantity.as_decimal),
                    current_price=Money(
                        amount=pos.current_price.as_decimal,
                        currency=pos.current_price.currency,
                    ),
                ),
            )

        return Portfolio(
            total_amount=total_amount,
            amounts_by_category=amounts_by_category,
            positions=positions,
        )
