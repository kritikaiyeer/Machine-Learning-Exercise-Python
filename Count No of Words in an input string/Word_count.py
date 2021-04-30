# counting Number of Words in a given string

# Cleaning Punctuation function
def cleaning_punctuation(user_string):
	# Cleaning text and lower casing all words
	for char in '-.,\n()':
		user_string = user_string.replace(char,' ')
	user_string = user_string.lower()
	return user_string

# word Count function : Basic Split function 
def word_count(user_string):
	user_string = cleaning_punctuation(user_string)
	count = len(user_string.split())
	return str(count)


if __name__ == "__main__":
	# Test string 	
	test_string = "This is a Test String"
	# printing original string 
	print("[+] The Test string is : " + test_string)
	print("[+] The number of words in Test string are : " + word_count(test_string))

	user_string = input(" \n\n[-]Enter the String you want Word count of = ")
	print("----------------------------------------------------------------------------------")
	print("\n\n[+] The Given string is : " + user_string)
	print("\n[+] The number of words in Test string are : " + word_count(user_string))



