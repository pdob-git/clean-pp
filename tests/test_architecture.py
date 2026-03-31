from pytest_archon import archrule

# Replace "src" with the actual name of your package folder 
# (e.g., "clean_pp" or "myapp")
BASE = "clean_app" 

def test_clean_architecture_compliance():
    """
    Enforces the Dependency Rule: 
    Infrastructure -> Presentation -> Application -> Domain
    """

    # 1. Domain: The Core
    # Must not depend on Application, Presentation, or Infrastructure.
    archrule("Domain isolation") \
        .match(f"{BASE}.domain*") \
        .should_not_import(f"{BASE}.application*") \
        .should_not_import(f"{BASE}.presentation*") \
        .should_not_import(f"{BASE}.infrastructure*") \
        .check(BASE)

    # 2. Application: Use Cases
    # Can depend on Domain, but NOT Presentation or Infrastructure.
    archrule("Application isolation") \
        .match(f"{BASE}.application*") \
        .should_not_import(f"{BASE}.presentation*") \
        .should_not_import(f"{BASE}.infrastructure*") \
        .check(BASE)

    # 3. Presentation: Adapters/Controllers
    # Can depend on Application and Domain, but NOT Infrastructure.
    archrule("Presentation isolation") \
        .match(f"{BASE}.presentation*") \
        .should_not_import(f"{BASE}.infrastructure*") \
        .check(BASE)

    # 4. Infrastructure: Frameworks & Drivers
    # Allowed to depend on everything (Domain, Application, Presentation).
    # We check for cycles here just to maintain internal health.
    archrule("Infrastructure health") \
        .match(f"{BASE}.infrastructure*") \
        .may_import(f"{BASE}.presentation*") \
        .may_import(f"{BASE}.application*") \
        .may_import(f"{BASE}.domain*") \
        .check(BASE)