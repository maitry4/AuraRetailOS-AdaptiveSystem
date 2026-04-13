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
aura-retail-os/
├── core/
│   ├── KioskInterface.py         # Facade — public API for all external interactions
│   ├── CentralRegistry.py        # Singleton — global config and status
│   └── EventBus.py               # Observer — event publish/subscribe system
│
├── kiosk/
│   ├── factory/
│   │   ├── KioskFactory.py       # Abstract Factory interface
│   │   ├── PharmacyKioskFactory.py
│   │   ├── FoodKioskFactory.py
│   │   └── EmergencyReliefKioskFactory.py
│   └── state/
│       ├── KioskState.py         # State pattern base
│       ├── ActiveState.py
│       ├── PowerSavingState.py
│       ├── MaintenanceState.py
│       └── EmergencyLockdownState.py
│
├── pricing/
│   ├── PricingPolicy.py          # Strategy interface
│   ├── StandardPricing.py
│   ├── DiscountedPricing.py
│   └── EmergencyPricing.py
│
├── transaction/
│   ├── Command.py                # Command interface
│   ├── PurchaseItemCommand.py
│   ├── RefundCommand.py
│   ├── RestockCommand.py
│   └── TransactionSnapshot.py   # Memento for rollback
│
├── hardware/
│   ├── Dispenser.py              # Hardware abstraction interface
│   ├── SpiralDispenser.py
│   └── RoboticArmDispenser.py
│
├── failure/
│   ├── FailureHandler.py         # Chain of Responsibility base
│   ├── RetryHandler.py
│   ├── RecalibrationHandler.py
│   └── TechnicianAlertHandler.py
│
├── inventory/
│   ├── InventoryManager.py
│   └── Product.py
│
├── persistence/
│   ├── inventory.json
│   ├── transactions.json
│   └── config.json
│
├── simulation/
│   └── scenarios.py              # Runnable demo scenarios
│
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

### Run the simulation

```bash
python simulation/scenarios.py
```

This executes all three demo scenarios sequentially and prints a structured log of system events, state transitions, and transaction outcomes.

### Run a specific scenario

```bash
python simulation/scenarios.py --scenario emergency
python simulation/scenarios.py --scenario hardware_failure
python simulation/scenarios.py --scenario dynamic_pricing
```

---

## Simulation Scenarios

### 1. Emergency Mode Activation
- Kiosk receives `EmergencyModeActivated` event via EventBus
- State transitions from `ActiveState` → `EmergencyLockdownState`
- Purchase quantity limits are enforced
- Emergency pricing policy is applied automatically

### 2. Hardware Failure Recovery
- Dispenser fails mid-transaction
- `FailureHandler` chain fires: retry → recalibrate → technician alert
- `TransactionSnapshot` (Memento) rolls back inventory and payment state
- `HardwareFailureEvent` is published to city monitoring subscribers

### 3. Dynamic Pricing Change
- Admin triggers a pricing policy switch at runtime
- Kiosk swaps from `StandardPricing` to `DiscountedPricing` via Strategy pattern
- All subsequent `purchaseItem()` calls compute prices using the new policy
- No restart or code change required

---

## Persistence

The system reads and writes state to JSON files under `persistence/`:

| File | Contents |
|---|---|
| `inventory.json` | Product catalog, stock counts, hardware dependencies |
| `transactions.json` | Command execution log with timestamps and outcomes |
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
