function App() {
  return (
    <div className="min-h-full bg-gradient-to-b from-gray-900 to-indigo-900">
      <nav className="bg-black/30 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center">
              <div className="text-white text-2xl font-bold font-medieval">Game of Thrones</div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <a href="#" className="text-gray-300 hover:bg-white/10 hover:text-white rounded-md px-3 py-2 transition-all">
                    Seasons
                  </a>
                  <a href="#" className="text-gray-300 hover:bg-white/10 hover:text-white rounded-md px-3 py-2 transition-all">
                    Archive
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="relative">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative mx-auto max-w-7xl py-12 sm:py-20 px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl sm:text-6xl font-bold text-white mb-8 tracking-tight">
              Welcome to
              <span className="block text-5xl sm:text-7xl bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mt-2">
                Game of Thrones
              </span>
            </h1>

            <div className="max-w-3xl mx-auto">
              <p className="mt-6 text-lg sm:text-xl leading-8 text-gray-300">
                Enter a world of strategic conquest where teams battle for control over mysterious cubes
                in an epic game of territory and timing.
              </p>

              <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
                <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
                  <h3 className="text-xl font-semibold text-white mb-3">Strategic Gameplay</h3>
                  <p className="text-gray-300">
                    Coordinate with your team to capture and defend valuable cubes. Time your moves perfectly
                    to maximize points and outmaneuver your opponents.
                  </p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
                  <h3 className="text-xl font-semibold text-white mb-3">Seasonal Competitions</h3>
                  <p className="text-gray-300">
                    Compete in seasonal tournaments, climb the leaderboards, and prove your team's supremacy
                    in this unique blend of strategy and timing.
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-12 flex items-center justify-center gap-x-6">
              <a
                href="#"
                className="rounded-md bg-gradient-to-r from-purple-500 to-indigo-600 px-5 py-3 text-base font-semibold text-white shadow-sm hover:from-purple-600 hover:to-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-all"
              >
                Start Playing
              </a>
              <a
                href="#"
                className="rounded-md px-5 py-3 text-base font-semibold text-gray-300 hover:text-white transition-colors"
              >
                Learn the Rules
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
