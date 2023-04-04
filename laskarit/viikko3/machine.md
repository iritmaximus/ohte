# Machine sequence diagram thing

```mermaid
sequenceDiagram

    Somefunction->>+Machine: Machine()
    Machine->>+FuelTank: FuelTank()
    Machine->>+Engine: Engine(tank)
    FuelTank->>-Machine: tank(0)
    Engine->>-Machine: engine()
    Machine->>-Somefunction: Jei

```
