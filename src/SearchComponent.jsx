import { useEffect, useState } from "react";

function SearchComponent() {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
      const data = await response.json();
      setIsLoading(false);
      setSearchResults(data.results);
    } catch (error) {
      setIsLoading(false);
      console.error("Error fetching search results:", error);
    }
  };

  useEffect(() => {
    console.log("coba");
  }, [searchResults]);

  return (
    <>
      <form className="w-full lg:w-1/2 " onSubmit={handleSearch}>
        <label
          htmlFor="default-search"
          className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
        >
          Search
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg
              className="w-4 h-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 20"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
              />
            </svg>
          </div>
          <input
            type="search"
            id="default-search"
            className="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search Title, Abstract"
            onChange={(e) => setQuery(e.target.value)}
            value={query}
            required
          />
          <button
            type="submit"
            className="text-black absolute end-2.5 bottom-2.5 bg-white  hover:text-black focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 "
            onClick={handleSearch}
          >
            Search
          </button>
        </div>
      </form>
      <div className="pt-5">
        {isLoading ? (
          <p className="text-center">Loading...</p>
        ) : searchResults.length <= 0 ? null : (
          searchResults.map((result, index) => (
            <a
              key={index}
              href={result.document[2]}
              target="_blank"
              className="block  p-6 bg-white border border-gray-200  shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
              rel="noreferrer"
            >
              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                {result.document[0]}
              </h5>
              <p className="font-normal text-gray-700 dark:text-gray-400">{result.document[1]}</p>
            </a>
          ))
        )}
      </div>
    </>
  );
}

export default SearchComponent;
