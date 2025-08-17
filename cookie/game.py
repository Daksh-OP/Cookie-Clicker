def redeem_code(code, state):
    # Define secret codes here
    if code == "GIMMEALL":
        state["cookies"] = 999999
        state["upgrades"]["cursor"] = 100
        state["upgrades"]["grandma"] = 50
        state["upgrades"]["factory"] = 20
        print("🎁 Redeem successful! You now have EVERYTHING!")
    else:
        print("❌ Invalid code")
