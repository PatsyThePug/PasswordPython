import streamlit as st
import random
import string
import pyperclip

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    """
    Generate a password using for loops and random module.
    
    Args:
        length (int): Length of the password
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_numbers (bool): Include numbers
        use_symbols (bool): Include symbols
    
    Returns:
        str: Generated password
    """
    # Build character set based on user preferences
    characters = ""
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Return empty string if no character sets selected
    if not characters:
        return ""
    
    # Generate password using for loop
    password = ""
    for i in range(length):
        random_index = random.randint(0, len(characters) - 1)
        password += characters[random_index]
    
    return password

def generate_multiple_passwords(count, length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    """
    Generate multiple passwords using for loop.
    
    Args:
        count (int): Number of passwords to generate
        length (int): Length of each password
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_numbers (bool): Include numbers
        use_symbols (bool): Include symbols
    
    Returns:
        list: List of generated passwords
    """
    passwords = []
    for i in range(count):
        password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
        if password:  # Only add if password generation was successful
            passwords.append(password)
    
    return passwords

def copy_to_clipboard(text):
    """
    Copy text to clipboard using pyperclip.
    
    Args:
        text (str): Text to copy to clipboard
    """
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False

def main():
    # Page configuration
    st.set_page_config(
        page_title="Password Generator",
        page_icon="🔐",
        layout="centered"
    )
    
    # Main title
    st.title("🔐 Password Generator")
    st.markdown("Generate secure passwords with customizable options")
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Configuration")
        
        # Password length slider
        length = st.slider(
            "Password Length",
            min_value=4,
            max_value=50,
            value=12,
            help="Select the length of your password"
        )
        
        # Number of passwords to generate
        count = st.number_input(
            "Number of Passwords",
            min_value=1,
            max_value=10,
            value=1,
            help="How many passwords to generate"
        )
    
    with col2:
        st.subheader("Character Sets")
        
        # Character set options
        use_uppercase = st.checkbox("Uppercase Letters (A-Z)", value=True)
        use_lowercase = st.checkbox("Lowercase Letters (a-z)", value=True)
        use_numbers = st.checkbox("Numbers (0-9)", value=True)
        use_symbols = st.checkbox("Symbols (!@#$%^&*)", value=False)
    
    # Validation
    if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
        st.error("❌ Please select at least one character set!")
        return
    
    # Generate button
    if st.button("🎲 Generate Password(s)", type="primary"):
        with st.spinner("Generating passwords..."):
            passwords = generate_multiple_passwords(
                count, length, use_uppercase, use_lowercase, use_numbers, use_symbols
            )
        
        if passwords:
            st.success(f"✅ Generated {len(passwords)} password(s)!")
            
            # Display generated passwords
            st.subheader("Generated Passwords")
            
            for i, password in enumerate(passwords, 1):
                # Create columns for password display and copy button
                pass_col1, pass_col2 = st.columns([4, 1])
                
                with pass_col1:
                    if count > 1:
                        st.code(f"{i}. {password}", language="text")
                    else:
                        st.code(password, language="text")
                
                with pass_col2:
                    if st.button("📋", key=f"copy_{i}", help="Copy to clipboard"):
                        if copy_to_clipboard(password):
                            st.success("Copied!", icon="✅")
                        else:
                            st.error("Copy failed", icon="❌")
            
            # Password strength indicator
            st.subheader("Password Strength")
            strength_score = 0
            strength_factors = []
            
            # Calculate strength based on character sets and length
            if use_uppercase:
                strength_score += 1
                strength_factors.append("Uppercase letters")
            if use_lowercase:
                strength_score += 1
                strength_factors.append("Lowercase letters")
            if use_numbers:
                strength_score += 1
                strength_factors.append("Numbers")
            if use_symbols:
                strength_score += 2
                strength_factors.append("Special symbols")
            
            if length >= 12:
                strength_score += 2
                strength_factors.append("Good length (12+ characters)")
            elif length >= 8:
                strength_score += 1
                strength_factors.append("Adequate length (8+ characters)")
            
            # Display strength
            if strength_score >= 6:
                st.success("🛡️ **Strong Password**")
                strength_color = "green"
            elif strength_score >= 4:
                st.warning("⚠️ **Medium Strength Password**")
                strength_color = "orange"
            else:
                st.error("🚨 **Weak Password**")
                strength_color = "red"
            
            # Show strength factors
            st.write("**Strength factors:**")
            for factor in strength_factors:
                st.write(f"• {factor}")
        
        else:
            st.error("❌ Failed to generate passwords. Please check your settings.")
    
    # Information section
    with st.expander("ℹ️ About This Generator"):
        st.markdown("""
        This password generator uses Python's `random` module and `for` loops to create secure passwords.
        
        **Features:**
        - Customizable password length (4-50 characters)
        - Multiple character sets (uppercase, lowercase, numbers, symbols)
        - Generate multiple passwords at once
        - Copy to clipboard functionality
        - Password strength assessment
        
        **Security Tips:**
        - Use passwords with at least 12 characters
        - Include a mix of character types
        - Avoid using personal information
        - Use unique passwords for each account
        - Consider using a password manager
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Made with ❤️ using Streamlit</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
