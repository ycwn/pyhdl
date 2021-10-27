

; SEE YOU AT THE PARTY RICHTER
main:
	LDA 'H'
	STA D
	LDN A
	STD @A

	LDA 'e'
	STA D
	LDN A
	STD @A

	LDA 'l'
	STA D
	LDN A
	STD @A

	LDA 'l'
	STA D
	LDN A
	STD @A

	LDA 'o'
	STA D
	LDN A
	STD @A

	LDA ' '
	STA D
	LDN A
	STD @A

	LDA 'W'
	STA D
	LDN A
	STD @A

	LDA 'o'
	STA D
	LDN A
	STD @A

	LDA 'r'
	STA D
	LDN A
	STD @A

	LDA 'l'
	STA D
	LDN A
	STD @A

	LDA 'd'
	STA D
	LDN A
	STD @A

	LDA '!'
	STA D
	LDN A
	STD @A

	LDA 10
	STA D
	LDN A
	STD @A

	LDA done
done:
	JMP

