import static spark.Spark.*;

public class Main {
    public static void main(String[] args) {

        port(Integer.parseInt(
            System.getenv().getOrDefault("PORT", "8080")
        ));

        get("/add", (req, res) -> {
            int a = Integer.parseInt(req.queryParams("a"));
            int b = Integer.parseInt(req.queryParams("b"));
            return String.valueOf(a + b);
        });

        get("/", (req, res) -> "Java Add API Running");
    }
}
