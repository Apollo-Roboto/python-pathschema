/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./index.html"],
	theme: {
		fontFamily: {
			'sans': ['Inter'],
			'mono': ['Fira Code']
		},
		extend: {
		},
	},
	plugins: [
		require('tailwind-scrollbar'),
	],
}
