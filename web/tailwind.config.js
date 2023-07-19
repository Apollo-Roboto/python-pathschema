/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./**/*.{html,js,ts}"],
	theme: {
		extend: {
		},
	},
	plugins: [
		require('tailwind-scrollbar'),
	],
}
