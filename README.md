# Aura Retail OS

> **IT620 — Object Oriented Programming | Path A: Adaptive Autonomous System**

Aura Retail OS is a modular, event-driven platform for managing autonomous retail kiosks deployed across the smart city of Zephyrus. Kiosks operate in hospitals, metro stations, university campuses, and disaster zones — each sharing the same hardware but running under different policies, pricing rules, and operational modes.

---

## Table of Contents

- [System Overview](#system-overview)
- [Architecture](#architecture)
- [Design Patterns](#design-patterns)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Simulation Scenarios](#simulation-scenarios)
- [Team Members](#team-members)

---

## System Overview

Aura Retail OS replaces the brittle monolithic Aura-Kiosk v1.0 with a platform that can:

- Switch pricing strategies at runtime (standard, discounted, emergency)
- Transition between kiosk operational modes (Active, Power-Saving, Maintenance, Emergency Lockdown)
- Handle hardware and transaction failures through a chain of automated recovery handlers
- Roll back transactions atomically if dispensing fails mid-operation
- Communicate between subsystems via a decoupled event notification system

---

## Architecture

The system is organized into five subsystems:

```
Aura Retail OS
├── Kiosk Core System         # User interaction, operational modes, kiosk lifecycle
├── Inventory System          # Products, bundles, stock levels, derived availability
├── Payment System            # Transaction commands, provider abstraction
├── Hardware Abstraction Layer # Dispensers, sensors, motors (via interfaces)
└── City Monitoring System    # Event subscribers: alerts, supply chain, monitoring
```

All subsystems communicate through an **EventBus** (Observer pattern). No subsystem holds a direct reference to another subsystem's concrete classes.

---

## Design Patterns

| Pattern | Where Used |
|---|---|
| **Strategy** | `PricingPolicy` — swap standard / discounted / emergency pricing at runtime |
| **State** | `KioskState` — Active, PowerSaving, Maintenance, EmergencyLockdown modes |
| **Chain of Responsibility** | `FailureHandler` chain — retry → recalibrate → alert technician |
| **Observer / Event Bus** | `EventBus` — LowStockEvent, HardwareFailureEvent, EmergencyModeActivated |
| **Command** | `PurchaseItemCommand`, `RefundCommand`, `RestockCommand` — executable + loggable |
| **Memento** | `TransactionSnapshot` — saves state before dispensing; restores on failure |
| **Abstract Factory** | `KioskFactory` — creates PharmacyKiosk, FoodKiosk, EmergencyReliefKiosk with compatible components |
| **Facade** | `KioskInterface` — single entry point: `purchaseItem()`, `refundTransaction()`, `runDiagnostics()`, `restockInventory()` |
| **Singleton** | `CentralRegistry` — global config and system status |

---

## Project Structure

```
AuraRetailOS-AdaptiveSystem/
├── commands/
│   ├── command.py                # Command interface
│   ├── purchase_item_command.py
│   ├── refund_command.py
│   └── restock_command.py
│
├── core/
│   ├── central_registry.py       # Singleton — global config and status
│   ├── kiosk_core.py             # Core logic for the kiosk
│   └── kiosk_interface.py        # Facade — public API for all external interactions
│
├── data/
│   ├── config.json               # Kiosk configuration
│   ├── inventory.json            # Product catalog and stock counts
│   └── transactions.csv          # Command execution log
│
├── events/
│   ├── emergency_mode_activated.py
│   ├── event_bus.py              # Observer — event publish/subscribe system
│   ├── hardware_failure_event.py
│   ├── low_stock_event.py
│   └── transaction_completed.py
│
├── external/
│   ├── city_monitoring_center.py
│   ├── maintenance_service.py
│   └── supply_chain_system.py
│
├── factory/
│   ├── emergency_kiosk_factory.py
│   ├── food_kiosk_factory.py
│   ├── kiosk_factory.py          # Abstract Factory interface
│   └── pharmacy_kiosk_factory.py
│
├── failure/
│   ├── auto_retry_handler.py
│   ├── failure_handler.py        # Chain of Responsibility base
│   ├── recalibration_handler.py
│   └── technician_alert_handler.py
│
├── hardware/
│   ├── dispenser.py              # Hardware abstraction interface
│   ├── hardware_controller.py
│   ├── sensor_module.py
│   └── verification_module.py
│
├── inventory/
│   ├── emergency_inventory_policy.py
│   ├── inventory_manager.py
│   ├── inventory_policy.py
│   └── standard_inventory_policy.py
│
├── memento/
│   └── state_snapshot.py         # Memento for rollback
│
├── modes/
│   ├── active_mode.py
│   ├── emergency_lockdown_mode.py
│   ├── kiosk_mode.py             # State pattern base
│   ├── maintenance_mode.py
│   └── power_saving_mode.py
│
├── persistence/
│   └── persistence_service.py
│
├── pricing/
│   ├── discounted_pricing.py
│   ├── emergency_pricing.py
│   ├── pricing_strategy.py       # Strategy interface
│   └── standard_pricing.py
│
├── main.py                       # Application entry point
├── index.html                    # Frontend UI
├── requirements.txt              # Dependencies
└── README.md
```

---

## How to Run

### Prerequisites

- Python 3.10+
- No external dependencies (standard library only)

### Setup

```bash
git clone https://github.com/<your-org>/AuraRetailOS-AdaptiveSystem.git
cd AuraRetailOS-AdaptiveSystem
```

### Run the interactive system
```bash
python main.py
```
This launches a CLI menu that allows you to manage multiple kiosks, simulate city-wide events, and observe the design patterns in real-time.

---

## Simulation Scenarios

### 1. High Stock Adaptive Pricing (Strategy Pattern)
1. Select **Scenario: Adaptive Pricing** or create a kiosk with >15 items.
2. Observe the system automatically recommending `DiscountedPricing`.
3. Perform a purchase and see the 15% discount applied in the transaction log.

### 2. City-Wide Emergency (Observer & State Patterns)
1. Select **Option 6: Trigger City-Wide Emergency**.
2. The `CentralRegistry` activates the emergency flag.
3. The `EventBus` broadcasts a priority `EmergencyModeActivated` signal.
4. **Result**: All registered kiosks (Pharmacy, Food, etc.) instantly transition to `EMERGENCY_LOCKDOWN` mode.
5. Try to buy a non-essential item (e.g., Chips) in lockdown; the system will deny it.

### 3. Hardware Self-Healing (Chain of Responsibility & Memento)
1. Select **Option 7: Simulate Hardware Failure**.
2. The system builds a faulty kiosk and attempts a purchase.
3. A "Motor Stall" is detected. The `FailureHandler` chain attempts recovery:
   - `AutoRetry` attempts to fix the stall.
   - `Recalibration` attempts to align the motor.
   - `TechnicianAlert` is finally triggered.
4. **Result**: The `PurchaseItemCommand` detects the failure and uses the **Memento** (`StateSnapshot`) to restore inventory perfectly.

### 4. Low Stock Alert (Event-Driven Monitoring)
1. Perform multiple purchases until a product's stock falls below 3.
2. Observe the `LowStockEvent` being published to the global monitor.
3. This demonstrates decoupled communication between the Inventory System and the Monitoring Center.

---

## Persistence

The system reads and writes state to files under `data/`:

| File | Contents |
|---|---|
| `inventory.json` | Product catalog, stock counts, hardware dependencies |
| `transactions.csv` | Command execution log with timestamps and outcomes |
| `config.json` | Kiosk type, active mode, pricing policy, emergency status |

State is loaded on startup and flushed after each successful transaction.

---

## Team Members

| Name | Assigned Subsystem | Key Responsibilities |
|---|---|---|
| **Maitry Parikh** | Kiosk Core System & Payment System | Kiosk operation flow, KioskInterface facade, transaction commands, payment integration |
| **Khushi Pal** | City Monitoring System & Event System | EventBus, CentralRegistry, system alerts, mode transitions |
| **Khushi Odedara** | Hardware Abstraction Layer | Dispenser abstraction, hardware module management, failure handler chain |
| **Hardik Kansara** | Inventory System | Stock tracking, derived available stock, inventory policies, bundle management |

---

*Course: IT620 Object Oriented Programming*
