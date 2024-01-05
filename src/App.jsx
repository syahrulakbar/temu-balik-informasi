import SearchComponent from "./SearchComponent";

function App() {
  return (
    <>
      <div className="p-5">
        <h1 className="text-xl font-semibold flex w-full justify-center">Temu Balik Informasi</h1>
      </div>
      <div className="w-full flex justify-center flex-col items-center">
        <SearchComponent />
      </div>
    </>
  );
}

export default App;
