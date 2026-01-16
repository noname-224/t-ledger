from t_ledger.application.services.bond.base import BondServiceMixin
from t_ledger.domain.enums.core import RiskLevel
from t_ledger.domain.interfaces.services import BondRiskService
from t_ledger.domain.models.core import BondsByRiskLevel


class BondRiskServiceImpl(BondServiceMixin, BondRiskService):
    async def get_bonds_by_risks(self) -> list[BondsByRiskLevel]:
        bonds = await self._build_bonds()

        bonds_by_risk_levels = {risk_level: [] for risk_level in RiskLevel}

        for bond in bonds:
            bonds_by_risk_levels[bond.risk_level].append(bond)

        return [
            BondsByRiskLevel(
                risk_level=risk_level,
                bonds=bonds,
            )
            for risk_level, bonds in bonds_by_risk_levels.items()
            if bonds
        ]
